from decimal import Decimal
from sqlalchemy import select
from fastapi import APIRouter, Depends
from redis import asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.infra.config import get_settings
from app.schemas.api import (
    ExchangeOut,
    FundingHistoryOut,
    FundingOpportunityOut,
    FundingSnapshotOut,
    FuturesOpportunityOut,
    HealthResponse,
    InstrumentOut,
    SystemStatusOut,
)
from app.services.state import runtime_state
from app.storage.database import get_db_session
from app.storage.models import (
    Exchange,
    FundingCurrent,
    FundingHistory,
    FundingOpportunity,
    FuturesFuturesOpportunity,
    Instrument,
)

router = APIRouter()
settings = get_settings()


def annualized_from_interval(rate: Decimal, minutes: int | None) -> Decimal | None:
    if not minutes or minutes <= 0:
        return None
    periods = Decimal(525600) / Decimal(minutes)
    return rate * Decimal(100) * periods


@router.get("/health", response_model=HealthResponse)
async def health(db: AsyncSession = Depends(get_db_session)) -> HealthResponse:
    db_status = "ok"
    redis_status = "ok"
    try:
        await db.execute(select(1))
    except Exception:  # noqa: BLE001
        db_status = "degraded"
    try:
        client = redis.from_url(settings.redis_url)
        pong = await client.ping()
        await client.close()
        if pong is not True:
            redis_status = "degraded"
    except Exception:  # noqa: BLE001
        redis_status = "degraded"
    status = "ok" if db_status == "ok" and redis_status == "ok" else "degraded"
    return HealthResponse(status=status, db=db_status, redis=redis_status)


@router.get("/exchanges", response_model=list[ExchangeOut])
async def exchanges(db: AsyncSession = Depends(get_db_session)):
    rows = await db.execute(select(Exchange))
    return [ExchangeOut.model_validate(x, from_attributes=True) for x in rows.scalars().all()]


@router.get("/instruments", response_model=list[InstrumentOut])
async def instruments(db: AsyncSession = Depends(get_db_session), canonical_symbol: str | None = None):
    stmt = select(Instrument)
    if canonical_symbol:
        stmt = stmt.where(Instrument.canonical_symbol == canonical_symbol)
    rows = await db.execute(stmt)
    return [InstrumentOut.model_validate(x, from_attributes=True) for x in rows.scalars().all()]


@router.get("/opportunities/futures-futures", response_model=list[FuturesOpportunityOut])
async def futures_futures(db: AsyncSession = Depends(get_db_session)):
    buy_ex = Exchange.__table__.alias("buy_ex")
    sell_ex = Exchange.__table__.alias("sell_ex")
    rows = await db.execute(
        select(FuturesFuturesOpportunity, buy_ex.c.name, sell_ex.c.name)
        .join(buy_ex, buy_ex.c.id == FuturesFuturesOpportunity.buy_exchange_id)
        .join(sell_ex, sell_ex.c.id == FuturesFuturesOpportunity.sell_exchange_id)
        .order_by(FuturesFuturesOpportunity.ts.desc())
        .limit(200)
    )
    return [
        FuturesOpportunityOut(
            canonical_symbol=r.canonical_symbol,
            buy_exchange=buy_name,
            sell_exchange=sell_name,
            buy_ask=r.buy_ask,
            sell_bid=r.sell_bid,
            gross_spread_pct=r.gross_spread_pct,
            net_spread_pct=r.net_spread_pct,
            fee_estimate_pct=r.fee_estimate_pct,
            slippage_estimate_pct=r.slippage_estimate_pct,
            max_tradable_notional=r.max_tradable_notional,
            freshness_ms=r.freshness_ms,
            confidence_score=r.confidence_score,
            ts=r.ts,
        )
        for r, buy_name, sell_name in rows.all()
    ]


@router.get("/funding/current", response_model=list[FundingSnapshotOut])
async def funding_current(db: AsyncSession = Depends(get_db_session)):
    rows = await db.execute(
        select(FundingCurrent, Instrument, Exchange)
        .join(Instrument, Instrument.id == FundingCurrent.instrument_id)
        .join(Exchange, Exchange.id == Instrument.exchange_id)
    )
    return [
        FundingSnapshotOut(
            exchange=ex.name,
            canonical_symbol=inst.canonical_symbol,
            funding_rate=fc.funding_rate,
            annualized_funding_pct=annualized_from_interval(fc.funding_rate, fc.funding_interval_minutes),
            next_funding_time=fc.next_funding_time,
            funding_interval_minutes=fc.funding_interval_minutes,
            mark_price=fc.mark_price,
            ts=fc.ts,
        )
        for fc, inst, ex in rows.all()
    ]


@router.get("/funding/history", response_model=list[FundingHistoryOut])
async def funding_history(db: AsyncSession = Depends(get_db_session), canonical_symbol: str | None = None, limit: int = 200):
    stmt = (
        select(FundingHistory, Instrument, Exchange)
        .join(Instrument, Instrument.id == FundingHistory.instrument_id)
        .join(Exchange, Exchange.id == Instrument.exchange_id)
        .order_by(FundingHistory.funding_time.desc())
        .limit(limit)
    )
    if canonical_symbol:
        stmt = stmt.where(Instrument.canonical_symbol == canonical_symbol)
    rows = await db.execute(stmt)
    return [
        FundingHistoryOut(
            exchange=ex.name,
            canonical_symbol=inst.canonical_symbol,
            funding_time=fh.funding_time,
            funding_rate=fh.funding_rate,
            mark_price_optional=fh.mark_price_optional,
        )
        for fh, inst, ex in rows.all()
    ]


@router.get("/opportunities/funding", response_model=list[FundingOpportunityOut])
async def funding_opportunities(db: AsyncSession = Depends(get_db_session)):
    rec_ex = Exchange.__table__.alias("rec_ex")
    hed_ex = Exchange.__table__.alias("hed_ex")
    rows = await db.execute(
        select(FundingOpportunity, rec_ex.c.name, hed_ex.c.name)
        .join(rec_ex, rec_ex.c.id == FundingOpportunity.receive_exchange_id)
        .join(hed_ex, hed_ex.c.id == FundingOpportunity.hedge_exchange_id)
        .order_by(FundingOpportunity.ts.desc())
        .limit(200)
    )
    return [
        FundingOpportunityOut(
            canonical_symbol=r.canonical_symbol,
            receive_exchange=rec_name,
            hedge_exchange=hed_name,
            primary_leg_side=r.primary_leg_side,
            hedge_leg_side=r.hedge_leg_side,
            funding_receive_pct=r.funding_receive_pct,
            funding_pay_pct=r.funding_pay_pct,
            net_expected_pct=r.net_expected_pct,
            fee_estimate_pct=r.fee_estimate_pct,
            slippage_estimate_pct=r.slippage_estimate_pct,
            next_funding_time=r.next_funding_time,
            max_tradable_notional=r.max_tradable_notional,
            confidence_score=r.confidence_score,
            ts=r.ts,
        )
        for r, rec_name, hed_name in rows.all()
    ]


@router.get("/system/status", response_model=SystemStatusOut)
async def system_status():
    return SystemStatusOut(collector=runtime_state.collector_status, adapters=runtime_state.adapter_status)
