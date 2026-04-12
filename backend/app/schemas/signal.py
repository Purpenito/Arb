from datetime import datetime
from pydantic import BaseModel, Field

from app.models.enums import ArbitrageType, MarketType


class MarketLeg(BaseModel):
    exchange: str
    market_type: MarketType
    side: str = Field(description='LONG/SHORT or BUY/SELL')
    price: float
    top_size_usdt: float
    fee_pct: float
    funding_rate_pct: float | None = None
    link: str


class Signal(BaseModel):
    signal_id: str
    symbol: str
    arbitrage_type: ArbitrageType
    buy_or_long: MarketLeg
    sell_or_short: MarketLeg
    gross_spread_pct: float
    total_fees_pct: float
    net_profit_pct: float
    net_funding_edge_pct: float | None = None
    max_executable_size_usdt: float
    estimated_pnl_usdt: float
    liquidity_score: float
    updated_at: datetime


class SignalFilter(BaseModel):
    arbitrage_types: list[ArbitrageType] = []
    exchanges: list[str] = []
    coins: list[str] = []
    min_spread_pct: float | None = None
    min_net_profit_pct: float | None = None
    min_volume_usdt: float | None = None
    min_funding_edge_pct: float | None = None
    only_with_funding: bool = False
    search: str | None = None


class AlertRule(BaseModel):
    id: str
    min_net_profit_pct: float
    min_funding_edge_pct: float | None = None
    min_size_usdt: float
    coins: list[str] = []
    exchanges: list[str] = []
    arbitrage_types: list[ArbitrageType] = []
    channel: str
