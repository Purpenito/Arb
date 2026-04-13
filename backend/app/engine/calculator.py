from __future__ import annotations

from datetime import UTC, datetime
from itertools import combinations
from uuid import uuid4
import random

from app.adapters.base import ExchangeAdapter
from app.models.enums import ArbitrageType, MarketType
from app.schemas.signal import MarketLeg, Signal


class ArbitrageEngine:
    def __init__(self, adapters: list[ExchangeAdapter]):
        self.adapters = adapters

    async def scan(self) -> list[Signal]:
        exchange_symbols: dict[str, set[str]] = {}
        for adapter in self.adapters:
            exchange_symbols[adapter.name] = set(await adapter.fetch_symbols())

        shared_symbols: set[str] = set()
        for symbol in set().union(*exchange_symbols.values()):
            coverage = sum(1 for symbols in exchange_symbols.values() if symbol in symbols)
            if coverage >= 2:
                shared_symbols.add(symbol)

        signals: list[Signal] = []
        for symbol in sorted(shared_symbols):
            books = {a.name: await a.fetch_top_of_book(symbol) for a in self.adapters if symbol in exchange_symbols[a.name]}
            funding = {a.name: await a.fetch_funding(symbol) for a in self.adapters if symbol in exchange_symbols[a.name]}
            active_adapters = [a for a in self.adapters if symbol in exchange_symbols[a.name]]
            for left, right in combinations(active_adapters, 2):
                signals.extend([
                    self._spot_futures(symbol, left, right, books[left.name], books[right.name]),
                    self._futures_futures(symbol, left, right, books[left.name], books[right.name]),
                    self._funding(symbol, left, right, books[left.name], books[right.name], funding[left.name], funding[right.name]),
                ])
        return signals

    def _spot_futures(self, symbol, buy_ex, sell_ex, buy_book, sell_book) -> Signal:
        gross = ((sell_book.bid - buy_book.ask) / buy_book.ask) * 100
        fees = buy_ex.taker_fee_spot_pct + sell_ex.taker_fee_futures_pct
        net = gross - fees
        size = min(buy_book.ask_size_usdt, sell_book.bid_size_usdt)
        return self._build_signal(symbol, ArbitrageType.SPOT_FUTURES, buy_ex.name, sell_ex.name, MarketType.SPOT, MarketType.FUTURES, 'BUY', 'SELL', buy_book.ask, sell_book.bid, fees, gross, net, size, None)

    def _futures_futures(self, symbol, long_ex, short_ex, long_book, short_book) -> Signal:
        gross = ((short_book.bid - long_book.ask) / long_book.ask) * 100
        fees = long_ex.taker_fee_futures_pct + short_ex.taker_fee_futures_pct
        net = gross - fees
        size = min(long_book.ask_size_usdt, short_book.bid_size_usdt)
        return self._build_signal(symbol, ArbitrageType.FUTURES_FUTURES, long_ex.name, short_ex.name, MarketType.FUTURES, MarketType.FUTURES, 'LONG', 'SHORT', long_book.ask, short_book.bid, fees, gross, net, size, None)

    def _funding(self, symbol, long_ex, short_ex, long_book, short_book, long_funding, short_funding) -> Signal:
        gross = ((short_book.bid - long_book.ask) / long_book.ask) * 100
        fees = long_ex.taker_fee_futures_pct + short_ex.taker_fee_futures_pct
        funding_edge = (short_funding.funding_rate_pct if short_funding else 0) - (long_funding.funding_rate_pct if long_funding else 0)
        net = gross - fees + funding_edge
        size = min(long_book.ask_size_usdt, short_book.bid_size_usdt)
        return self._build_signal(symbol, ArbitrageType.FUNDING, long_ex.name, short_ex.name, MarketType.FUTURES, MarketType.FUTURES, 'LONG', 'SHORT', long_book.ask, short_book.bid, fees, gross, net, size, funding_edge)

    def _build_signal(self, symbol, arb_type, buy_exchange, sell_exchange, buy_market, sell_market, buy_side, sell_side, buy_price, sell_price, fees, gross, net, size, funding_edge) -> Signal:
        spread_history = [round(gross + random.uniform(-0.18, 0.18), 3) for _ in range(16)]
        spread_history[-1] = round(gross, 3)
        return Signal(
            signal_id=str(uuid4()),
            symbol=symbol,
            arbitrage_type=arb_type,
            buy_or_long=MarketLeg(exchange=buy_exchange, market_type=buy_market, side=buy_side, price=buy_price, top_size_usdt=size, fee_pct=fees / 2, funding_rate_pct=funding_edge if arb_type == ArbitrageType.FUNDING else None, link=''),
            sell_or_short=MarketLeg(exchange=sell_exchange, market_type=sell_market, side=sell_side, price=sell_price, top_size_usdt=size, fee_pct=fees / 2, funding_rate_pct=funding_edge if arb_type == ArbitrageType.FUNDING else None, link=''),
            gross_spread_pct=round(gross, 4),
            total_fees_pct=round(fees, 4),
            net_profit_pct=round(net, 4),
            net_funding_edge_pct=round(funding_edge, 4) if funding_edge is not None else None,
            max_executable_size_usdt=round(size, 2),
            estimated_pnl_usdt=round(size * (net / 100), 2),
            liquidity_score=round(size / 10_000, 2),
            spread_history_pct=spread_history,
            signal_lifetime_sec=random.randint(40, 5400),
            updated_at=datetime.now(UTC),
        )
