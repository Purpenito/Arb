from __future__ import annotations

import random

from app.adapters.base import ExchangeAdapter, FundingSnapshot, TopOfBook


class MockExchangeAdapter(ExchangeAdapter):
    def __init__(self, name: str, fee_spot: float, fee_futures: float, base_url: str):
        self.name = name
        self.taker_fee_spot_pct = fee_spot
        self.taker_fee_futures_pct = fee_futures
        self._base_url = base_url

    async def fetch_symbols(self) -> list[str]:
        return ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']

    async def fetch_top_of_book(self, symbol: str) -> TopOfBook:
        anchor = {'BTCUSDT': 70000, 'ETHUSDT': 3800, 'SOLUSDT': 160}.get(symbol, 100)
        noise = random.uniform(-0.004, 0.004)
        mid = anchor * (1 + noise)
        spread = mid * 0.0004
        return TopOfBook(
            symbol=symbol,
            bid=mid - spread,
            ask=mid + spread,
            bid_size_usdt=random.uniform(30_000, 450_000),
            ask_size_usdt=random.uniform(30_000, 450_000),
        )

    async def fetch_funding(self, symbol: str) -> FundingSnapshot | None:
        return FundingSnapshot(symbol=symbol, funding_rate_pct=random.uniform(-0.02, 0.03))

    def build_trading_link(self, symbol: str, market_type: str) -> str:
        return f'{self._base_url}/{market_type}/{symbol}'


ADAPTERS: list[ExchangeAdapter] = [
    MockExchangeAdapter('Binance', 0.10, 0.04, 'https://www.binance.com/en/trade'),
    MockExchangeAdapter('Bybit', 0.10, 0.055, 'https://www.bybit.com/trade'),
    MockExchangeAdapter('OKX', 0.08, 0.05, 'https://www.okx.com/trade-swap'),
]
