export type HealthResponse = { status: string; db: string; redis: string };

export type FuturesOpportunity = {
  canonical_symbol: string;
  buy_exchange: string;
  sell_exchange: string;
  buy_ask: string;
  sell_bid: string;
  gross_spread_pct: string;
  net_spread_pct: string;
  max_tradable_notional: string;
  freshness_ms: number;
  confidence_score: string;
  ts: string;
};

export type FundingOpportunity = {
  canonical_symbol: string;
  receive_exchange: string;
  hedge_exchange: string;
  funding_receive_pct: string;
  funding_pay_pct: string;
  net_expected_pct: string;
  next_funding_time: string | null;
  confidence_score: string;
  ts: string;
};

export type FundingCurrent = {
  exchange: string;
  canonical_symbol: string;
  funding_rate: string;
  annualized_funding_pct: string | null;
  next_funding_time: string | null;
  funding_interval_minutes: number | null;
  mark_price: string | null;
  ts: string;
};

export type SystemStatus = { collector: string; adapters: Record<string, string> };
