from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from app.core.symbols import canonical_symbol
from app.core.types import CanonicalInstrument, ContractType, FundingSnapshot, InstrumentType, TopOfBook
from app.exchange_adapters.base import ExchangeAdapter


def _to_decimal_or(default: Decimal, raw: str | int | float | None) -> Decimal:
    if raw is None:
        return default
    try:
        txt = str(raw).strip()
        if txt == "":
            return default
        return Decimal(txt)
    except (InvalidOperation, ValueError, TypeError):
        return default


def _to_decimal_or_none(raw: str | int | float | None) -> Decimal | None:
    if raw is None:
        return None
    try:
        txt = str(raw).strip()
        if txt == "":
            return None
        return Decimal(txt)
    except (InvalidOperation, ValueError, TypeError):
        return None


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
        return []

    async def ws_subscribe_top_of_book(self) -> None:
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
            tick_size=_to_decimal_or(Decimal("0.1"), tick_size),
            qty_step=_to_decimal_or(Decimal("0.001"), qty_step),
            min_qty=_to_decimal_or(Decimal("0.001"), min_qty),
            contract_size=_to_decimal_or(Decimal("1"), contract_size),
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
            bid=_to_decimal_or(Decimal("0"), bid),
            ask=_to_decimal_or(Decimal("0"), ask),
            bid_size=_to_decimal_or(Decimal("0"), bid_size),
            ask_size=_to_decimal_or(Decimal("0"), ask_size),
            mark_price=_to_decimal_or_none(mark),
            index_price=_to_decimal_or_none(index),
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
            funding_rate=_to_decimal_or(Decimal("0"), rate),
            mark_price=_to_decimal_or_none(mark_price),
            next_funding_time=next_funding_time,
            funding_interval_minutes=interval_minutes,
        )
