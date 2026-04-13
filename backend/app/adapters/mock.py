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
        return [
            'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'XRPUSDT', 'DOGEUSDT', 'ADAUSDT', 'AVAXUSDT',
            'LINKUSDT', 'LTCUSDT', 'DOTUSDT', 'BNBUSDT', 'TRXUSDT', 'NEARUSDT', 'UNIUSDT',
            'APTUSDT', 'ARBUSDT', 'OPUSDT', 'SUIUSDT', 'TIAUSDT', 'INJUSDT', 'ATOMUSDT',
        ]

    async def fetch_top_of_book(self, symbol: str) -> TopOfBook:
        anchors = {
            'BTCUSDT': 70000, 'ETHUSDT': 3800, 'SOLUSDT': 160, 'XRPUSDT': 1.1, 'DOGEUSDT': 0.22,
            'ADAUSDT': 0.85, 'AVAXUSDT': 45, 'LINKUSDT': 28, 'LTCUSDT': 95, 'DOTUSDT': 11,
            'BNBUSDT': 620, 'TRXUSDT': 0.18, 'NEARUSDT': 8, 'UNIUSDT': 13, 'APTUSDT': 14,
            'ARBUSDT': 2.1, 'OPUSDT': 2.8, 'SUIUSDT': 1.9, 'TIAUSDT': 13, 'INJUSDT': 39, 'ATOMUSDT': 12,
        }
        anchor = anchors.get(symbol, 100)
        noise = random.uniform(-0.006, 0.006)
        mid = anchor * (1 + noise)
        spread = mid * random.uniform(0.00025, 0.0008)
        liq_scale = 1.6 if symbol in {'BTCUSDT', 'ETHUSDT', 'SOLUSDT'} else 1.0
        return TopOfBook(
            symbol=symbol,
            bid=mid - spread,
            ask=mid + spread,
            bid_size_usdt=random.uniform(40_000, 800_000) * liq_scale,
            ask_size_usdt=random.uniform(40_000, 800_000) * liq_scale,
        )

    async def fetch_funding(self, symbol: str) -> FundingSnapshot | None:
        return FundingSnapshot(symbol=symbol, funding_rate_pct=random.uniform(-0.045, 0.055))

    def build_trading_link(self, symbol: str, market_type: str) -> str:
        return f'{self._base_url}/{market_type}/{symbol}'


ADAPTERS: list[ExchangeAdapter] = [
    MockExchangeAdapter('Binance', 0.10, 0.04, 'https://www.binance.com/en/trade'),
    MockExchangeAdapter('Bybit', 0.10, 0.055, 'https://www.bybit.com/trade'),
    MockExchangeAdapter('OKX', 0.08, 0.05, 'https://www.okx.com/trade-swap'),
    MockExchangeAdapter('KuCoin', 0.10, 0.06, 'https://www.kucoin.com/trade'),
    MockExchangeAdapter('Bitget', 0.10, 0.06, 'https://www.bitget.com/futures'),
    MockExchangeAdapter('BingX', 0.10, 0.05, 'https://bingx.com/en-us/futures'),
    MockExchangeAdapter('MEXC', 0.10, 0.05, 'https://www.mexc.com/exchange'),
    MockExchangeAdapter('Gate', 0.09, 0.05, 'https://www.gate.io/trade'),
    MockExchangeAdapter('HTX', 0.10, 0.06, 'https://www.htx.com/trade'),
]
