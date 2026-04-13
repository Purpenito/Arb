from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.types import FundingSnapshot, TopOfBook
from app.storage.models import BestQuote, Exchange, FundingCurrent, Instrument


class MarketRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_exchange(self, name: str) -> Exchange:
        row = await self.session.scalar(select(Exchange).where(Exchange.name == name))
        if row:
            return row
        row = Exchange(name=name)
        self.session.add(row)
        await self.session.flush()
        return row

    async def upsert_instrument(self, exchange_id: int, i) -> Instrument:
        row = await self.session.scalar(
            select(Instrument).where(
                Instrument.exchange_id == exchange_id,
                Instrument.native_symbol == i.native_symbol,
            )
        )
        payload = dict(
            canonical_symbol=i.canonical_symbol,
            base_asset=i.base_asset,
            quote_asset=i.quote_asset,
            settle_asset=i.settle_asset,
            contract_type=i.contract_type.value,
            instrument_type=i.instrument_type.value,
            tick_size=i.tick_size,
            qty_step=i.qty_step,
            min_qty=i.min_qty,
            contract_size=i.contract_size,
            funding_interval_minutes=i.funding_interval_minutes,
            is_active=True,
            raw_metadata_json=i.__dict__,
        )
        if row:
            for k, v in payload.items():
                setattr(row, k, v)
            return row
        row = Instrument(exchange_id=exchange_id, native_symbol=i.native_symbol, **payload)
        self.session.add(row)
        await self.session.flush()
        return row

    async def store_quotes(self, quotes: list[TopOfBook]) -> None:
        symbols = [q.canonical_symbol for q in quotes]
        instruments = await self.session.execute(select(Instrument).where(Instrument.canonical_symbol.in_(symbols)))
        inst_by_symbol = defaultdict(list)
        for i in instruments.scalars().all():
            inst_by_symbol[i.canonical_symbol].append(i)

        for q in quotes:
            inst_list = inst_by_symbol.get(q.canonical_symbol, [])
            for inst in inst_list:
                self.session.add(
                    BestQuote(
                        instrument_id=inst.id,
                        ts=q.ts,
                        bid=q.bid,
                        ask=q.ask,
                        bid_size=q.bid_size,
                        ask_size=q.ask_size,
                        mark_price=q.mark_price,
                        index_price=q.index_price,
                        is_stale=False,
                    )
                )

    async def store_funding(self, snapshots: list[FundingSnapshot]) -> None:
        symbols = [f.canonical_symbol for f in snapshots]
        instruments = await self.session.execute(select(Instrument).where(Instrument.canonical_symbol.in_(symbols)))
        inst_by_symbol = defaultdict(list)
        for i in instruments.scalars().all():
            inst_by_symbol[i.canonical_symbol].append(i)

        now = datetime.now(timezone.utc)
        for f in snapshots:
            for inst in inst_by_symbol.get(f.canonical_symbol, []):
                await self.session.execute(delete(FundingCurrent).where(FundingCurrent.instrument_id == inst.id))
                self.session.add(
                    FundingCurrent(
                        instrument_id=inst.id,
                        ts=now,
                        funding_rate=f.funding_rate,
                        next_funding_time=f.next_funding_time,
                        funding_interval_minutes=f.funding_interval_minutes,
                        mark_price=f.mark_price,
                        predicted_flag=f.predicted_flag,
                    )
                )
