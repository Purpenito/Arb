from abc import ABC, abstractmethod
from app.core.types import CanonicalInstrument, FundingSnapshot, TopOfBook


class ExchangeAdapter(ABC):
    name: str

    @abstractmethod
    async def fetch_instruments(self) -> list[CanonicalInstrument]:
        ...

    @abstractmethod
    async def fetch_current_funding(self) -> list[FundingSnapshot]:
        ...

    @abstractmethod
    async def fetch_funding_history(self, canonical_symbol: str, limit: int = 50) -> list[FundingSnapshot]:
        ...

    @abstractmethod
    async def fetch_top_of_book_snapshot(self) -> list[TopOfBook]:
        ...

    @abstractmethod
    async def ws_subscribe_top_of_book(self) -> None:
        ...
