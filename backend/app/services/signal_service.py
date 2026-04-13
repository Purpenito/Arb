from app.adapters.mock import ADAPTERS
from app.engine.calculator import ArbitrageEngine
from app.schemas.signal import Signal, SignalFilter


class SignalService:
    def __init__(self):
        self.engine = ArbitrageEngine(ADAPTERS)

    async def get_signals(self, filters: SignalFilter | None = None) -> list[Signal]:
        filters = filters or SignalFilter()
        signals = await self.engine.scan()
        enriched: list[Signal] = []
        for signal in signals:
            signal.buy_or_long.link = self._find_adapter(signal.buy_or_long.exchange).build_trading_link(signal.symbol, signal.buy_or_long.market_type.value)
            signal.sell_or_short.link = self._find_adapter(signal.sell_or_short.exchange).build_trading_link(signal.symbol, signal.sell_or_short.market_type.value)
            enriched.append(signal)
        return [s for s in enriched if self._accept(s, filters)]

    def _find_adapter(self, exchange: str):
        return next(adapter for adapter in ADAPTERS if adapter.name == exchange)

    def _accept(self, signal: Signal, f: SignalFilter) -> bool:
        coin = signal.symbol.replace('USDT', '')
        if f.arbitrage_types and signal.arbitrage_type not in f.arbitrage_types:
            return False
        if f.long_exchanges and signal.buy_or_long.exchange not in f.long_exchanges:
            return False
        if f.short_exchanges and signal.sell_or_short.exchange not in f.short_exchanges:
            return False
        if f.exchanges and (
            signal.buy_or_long.exchange not in f.exchanges and signal.sell_or_short.exchange not in f.exchanges
        ):
            return False
        if f.whitelist_coins and coin not in f.whitelist_coins:
            return False
        if f.blacklist_coins and coin in f.blacklist_coins:
            return False
        if f.min_spread_pct is not None and signal.gross_spread_pct < f.min_spread_pct:
            return False
        if f.min_net_profit_pct is not None and signal.net_profit_pct < f.min_net_profit_pct:
            return False
        if f.max_net_profit_pct is not None and signal.net_profit_pct > f.max_net_profit_pct:
            return False
        if f.min_volume_usdt is not None and signal.max_executable_size_usdt < f.min_volume_usdt:
            return False
        if f.max_volume_usdt is not None and signal.max_executable_size_usdt > f.max_volume_usdt:
            return False
        if f.min_funding_edge_pct is not None and (signal.net_funding_edge_pct or 0) < f.min_funding_edge_pct:
            return False
        if f.only_profitable and signal.net_profit_pct <= 0:
            return False
        if f.only_with_funding and signal.net_funding_edge_pct is None:
            return False
        if f.search and f.search.upper() not in signal.symbol:
            return False
        return True
