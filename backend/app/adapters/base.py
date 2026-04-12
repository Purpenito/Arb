from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(slots=True)
class TopOfBook:
    symbol: str
    bid: float
    ask: float
    bid_size_usdt: float
    ask_size_usdt: float


@dataclass(slots=True)
class FundingSnapshot:
    symbol: str
    funding_rate_pct: float


class ExchangeAdapter(ABC):
    name: str
    taker_fee_spot_pct: float
    taker_fee_futures_pct: float

    @abstractmethod
    async def fetch_symbols(self) -> list[str]: ...

    @abstractmethod
    async def fetch_top_of_book(self, symbol: str) -> TopOfBook: ...

    @abstractmethod
    async def fetch_funding(self, symbol: str) -> FundingSnapshot | None: ...

    @abstractmethod
    def build_trading_link(self, symbol: str, market_type: str) -> str: ...

    def normalize_symbol(self, symbol: str) -> str:
        return symbol.replace('-', '').replace('/', '').upper()
