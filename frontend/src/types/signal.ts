export type ArbitrageType = 'spot_futures' | 'futures_futures' | 'funding'

export interface Leg {
  exchange: string
  market_type: 'spot' | 'futures'
  side: 'LONG' | 'SHORT' | 'BUY' | 'SELL'
  price: number
  top_size_usdt: number
  fee_pct: number
  funding_rate_pct?: number | null
  link: string
}

export interface Signal {
  signal_id: string
  symbol: string
  arbitrage_type: ArbitrageType
  buy_or_long: Leg
  sell_or_short: Leg
  gross_spread_pct: number
  total_fees_pct: number
  net_profit_pct: number
  net_funding_edge_pct?: number | null
  max_executable_size_usdt: number
  estimated_pnl_usdt: number
  liquidity_score: number
  spread_history_pct: number[]
  signal_lifetime_sec: number
  updated_at: string
}

export interface FundingMonitorRow {
  symbol: string
  rates: Array<{ exchange: string; funding_rate_pct: number }>
  max_funding_spread_pct: number
}
