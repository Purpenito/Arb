from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from decimal import Decimal

from app.core.symbols import canonical_symbol
from app.core.types import CanonicalInstrument, ContractType, FundingSnapshot, InstrumentType, TopOfBook
from app.exchange_adapters.base import ExchangeAdapter


class RestPollingAdapter(ExchangeAdapter):
    name: str = "base"
    instruments_url: str
    ticker_url: str
    funding_url: str

    def __init__(self, timeout_seconds: int = 10) -> None:
        self.timeout_seconds = timeout_seconds

    async def _get_json(self, url: str) -> dict:
        import aiohttp
        timeout = aiohttp.ClientTimeout(total=self.timeout_seconds)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                return await resp.json()

    async def fetch_funding_history(self, canonical_symbol: str, limit: int = 50) -> list[FundingSnapshot]:
        # Many exchanges have unique history route shapes; keep v1 scoped to current funding.
        return []

    async def ws_subscribe_top_of_book(self) -> None:
        # Production deployment should run dedicated WS consumers; REST fallback exists for resiliency.
        await asyncio.sleep(0)

    def _to_instrument(
        self,
        native_symbol: str,
        base: str,
        quote: str,
        settle: str,
        *,
        contract_type: ContractType = ContractType.LINEAR,
        instrument_type: InstrumentType = InstrumentType.PERPETUAL,
        tick_size: str = "0.1",
        qty_step: str = "0.001",
        min_qty: str = "0.001",
        contract_size: str = "1",
        funding_interval_minutes: int = 480,
    ) -> CanonicalInstrument:
        return CanonicalInstrument(
            exchange=self.name,
            native_symbol=native_symbol,
            canonical_symbol=canonical_symbol(base, quote, settle),
            base_asset=base,
            quote_asset=quote,
            settle_asset=settle,
            contract_type=contract_type,
            instrument_type=instrument_type,
            tick_size=Decimal(tick_size),
            qty_step=Decimal(qty_step),
            min_qty=Decimal(min_qty),
            contract_size=Decimal(contract_size),
            funding_interval_minutes=funding_interval_minutes,
        )

    def _to_tob(
        self,
        canonical: str,
        bid: str,
        ask: str,
        bid_size: str,
        ask_size: str,
        mark: str | None = None,
        index: str | None = None,
    ) -> TopOfBook:
        return TopOfBook(
            exchange=self.name,
            canonical_symbol=canonical,
            ts=datetime.now(timezone.utc),
            bid=Decimal(bid),
            ask=Decimal(ask),
            bid_size=Decimal(bid_size),
            ask_size=Decimal(ask_size),
            mark_price=Decimal(mark) if mark else None,
            index_price=Decimal(index) if index else None,
        )

    def _to_funding(
        self,
        canonical: str,
        rate: str,
        mark_price: str | None,
        next_funding_time: datetime | None,
        interval_minutes: int | None,
    ) -> FundingSnapshot:
        return FundingSnapshot(
            exchange=self.name,
            canonical_symbol=canonical,
            ts=datetime.now(timezone.utc),
            funding_rate=Decimal(rate),
            mark_price=Decimal(mark_price) if mark_price else None,
            next_funding_time=next_funding_time,
            funding_interval_minutes=interval_minutes,
        )
