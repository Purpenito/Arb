CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE filter_presets (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  name TEXT NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE alert_rules (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL REFERENCES users(id),
  channel TEXT NOT NULL,
  payload JSONB NOT NULL,
  enabled BOOLEAN NOT NULL DEFAULT TRUE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE signal_history (
  id UUID PRIMARY KEY,
  symbol TEXT NOT NULL,
  arbitrage_type TEXT NOT NULL,
  buy_exchange TEXT NOT NULL,
  sell_exchange TEXT NOT NULL,
  gross_spread_pct DOUBLE PRECISION NOT NULL,
  net_profit_pct DOUBLE PRECISION NOT NULL,
  net_funding_edge_pct DOUBLE PRECISION,
  max_executable_size_usdt DOUBLE PRECISION NOT NULL,
  estimated_pnl_usdt DOUBLE PRECISION NOT NULL,
  liquidity_score DOUBLE PRECISION NOT NULL,
  first_seen_at TIMESTAMPTZ NOT NULL,
  last_seen_at TIMESTAMPTZ NOT NULL
);
