from datetime import datetime
from decimal import Decimal
from sqlalchemy import Boolean, DateTime, ForeignKey, Numeric, String, JSON, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Exchange(Base):
    __tablename__ = "exchanges"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    taker_fee_bps: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=5)
    maker_fee_bps: Mapped[Decimal] = mapped_column(Numeric(10, 4), default=2)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Instrument(Base):
    __tablename__ = "instruments"
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), index=True)
    native_symbol: Mapped[str] = mapped_column(String(100), index=True)
    canonical_symbol: Mapped[str] = mapped_column(String(100), index=True)
    base_asset: Mapped[str] = mapped_column(String(20))
    quote_asset: Mapped[str] = mapped_column(String(20))
    settle_asset: Mapped[str] = mapped_column(String(20))
    contract_type: Mapped[str] = mapped_column(String(20))
    instrument_type: Mapped[str] = mapped_column(String(20))
    tick_size: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    qty_step: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    min_qty: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    contract_size: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    funding_interval_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    raw_metadata_json: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class BestQuote(Base):
    __tablename__ = "best_quotes"
    id: Mapped[int] = mapped_column(primary_key=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"), index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    bid: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    ask: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    bid_size: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    ask_size: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    mark_price: Mapped[Decimal | None] = mapped_column(Numeric(30, 12), nullable=True)
    index_price: Mapped[Decimal | None] = mapped_column(Numeric(30, 12), nullable=True)
    last_price_optional: Mapped[Decimal | None] = mapped_column(Numeric(30, 12), nullable=True)
    is_stale: Mapped[bool] = mapped_column(Boolean, default=False)


class FundingCurrent(Base):
    __tablename__ = "funding_current"
    id: Mapped[int] = mapped_column(primary_key=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"), index=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    funding_rate: Mapped[Decimal] = mapped_column(Numeric(20, 12))
    next_funding_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    funding_interval_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mark_price: Mapped[Decimal | None] = mapped_column(Numeric(30, 12), nullable=True)
    predicted_flag: Mapped[bool] = mapped_column(Boolean, default=False)


class FundingHistory(Base):
    __tablename__ = "funding_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey("instruments.id"), index=True)
    funding_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    funding_rate: Mapped[Decimal] = mapped_column(Numeric(20, 12))
    mark_price_optional: Mapped[Decimal | None] = mapped_column(Numeric(30, 12), nullable=True)


class FuturesFuturesOpportunity(Base):
    __tablename__ = "futures_futures_opportunities"
    id: Mapped[int] = mapped_column(primary_key=True)
    canonical_symbol: Mapped[str] = mapped_column(String(100), index=True)
    buy_exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), index=True)
    sell_exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), index=True)
    buy_ask: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    sell_bid: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    gross_spread_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    fee_estimate_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    slippage_estimate_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    net_spread_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    max_tradable_notional: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    freshness_ms: Mapped[int] = mapped_column(Integer)
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class FundingOpportunity(Base):
    __tablename__ = "funding_opportunities"
    id: Mapped[int] = mapped_column(primary_key=True)
    canonical_symbol: Mapped[str] = mapped_column(String(100), index=True)
    receive_exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), index=True)
    hedge_exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), index=True)
    primary_leg_side: Mapped[str] = mapped_column(String(10))
    hedge_leg_side: Mapped[str] = mapped_column(String(10))
    funding_receive_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    funding_pay_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    fee_estimate_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    slippage_estimate_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    net_expected_pct: Mapped[Decimal] = mapped_column(Numeric(20, 8))
    next_funding_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    max_tradable_notional: Mapped[Decimal] = mapped_column(Numeric(30, 12))
    confidence_score: Mapped[Decimal] = mapped_column(Numeric(10, 6))
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)


class ConnectorState(Base):
    __tablename__ = "connector_state"
    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_id: Mapped[int] = mapped_column(ForeignKey("exchanges.id"), unique=True)
    status: Mapped[str] = mapped_column(String(20), default="ok")
    last_heartbeat: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    last_error: Mapped[str | None] = mapped_column(String(500), nullable=True)
