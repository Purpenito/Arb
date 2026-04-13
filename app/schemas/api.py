from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    db: str
    redis: str


class ExchangeOut(BaseModel):
    id: int
    name: str
    enabled: bool
    taker_fee_bps: Decimal
    maker_fee_bps: Decimal


class InstrumentOut(BaseModel):
    id: int
    exchange_id: int
    native_symbol: str
    canonical_symbol: str
    base_asset: str
    quote_asset: str
    settle_asset: str
    contract_type: str
    instrument_type: str
    funding_interval_minutes: int | None


class FuturesOpportunityOut(BaseModel):
    canonical_symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_ask: Decimal
    sell_bid: Decimal
    gross_spread_pct: Decimal
    net_spread_pct: Decimal
    fee_estimate_pct: Decimal
    slippage_estimate_pct: Decimal
    max_tradable_notional: Decimal
    freshness_ms: int
    confidence_score: Decimal
    ts: datetime


class FundingSnapshotOut(BaseModel):
    exchange: str
    canonical_symbol: str
    funding_rate: Decimal
    annualized_funding_pct: Decimal | None
    next_funding_time: datetime | None
    funding_interval_minutes: int | None
    mark_price: Decimal | None
    ts: datetime


class FundingHistoryOut(BaseModel):
    exchange: str
    canonical_symbol: str
    funding_time: datetime
    funding_rate: Decimal
    mark_price_optional: Decimal | None


class FundingOpportunityOut(BaseModel):
    canonical_symbol: str
    receive_exchange: str
    hedge_exchange: str
    primary_leg_side: str
    hedge_leg_side: str
    funding_receive_pct: Decimal
    funding_pay_pct: Decimal
    net_expected_pct: Decimal
    fee_estimate_pct: Decimal
    slippage_estimate_pct: Decimal
    next_funding_time: datetime | None
    max_tradable_notional: Decimal
    confidence_score: Decimal
    ts: datetime


class SystemStatusOut(BaseModel):
    collector: str
    adapters: dict[str, str]
