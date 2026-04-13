from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import StrEnum


class ContractType(StrEnum):
    LINEAR = "linear"
    INVERSE = "inverse"


class InstrumentType(StrEnum):
    PERPETUAL = "perpetual"
    FUTURES = "futures"


@dataclass(slots=True)
class CanonicalInstrument:
    exchange: str
    native_symbol: str
    canonical_symbol: str
    base_asset: str
    quote_asset: str
    settle_asset: str
    contract_type: ContractType
    instrument_type: InstrumentType
    tick_size: Decimal
    qty_step: Decimal
    min_qty: Decimal
    contract_size: Decimal
    funding_interval_minutes: int | None


@dataclass(slots=True)
class TopOfBook:
    exchange: str
    canonical_symbol: str
    ts: datetime
    bid: Decimal
    ask: Decimal
    bid_size: Decimal
    ask_size: Decimal
    mark_price: Decimal | None = None
    index_price: Decimal | None = None


@dataclass(slots=True)
class FundingSnapshot:
    exchange: str
    canonical_symbol: str
    ts: datetime
    funding_rate: Decimal
    next_funding_time: datetime | None
    funding_interval_minutes: int | None
    mark_price: Decimal | None = None
    predicted_flag: bool = False
