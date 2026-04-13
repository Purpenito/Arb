import { FundingMonitorRow, Signal } from '@/types/signal'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api/v1'

export interface SignalFilters {
  search?: string
  arbitrage_types?: string[]
  long_exchanges?: string[]
  short_exchanges?: string[]
  whitelist_coins?: string[]
  blacklist_coins?: string[]
  min_volume_usdt?: number
  max_volume_usdt?: number
  min_net_profit_pct?: number
  max_net_profit_pct?: number
  min_funding_edge_pct?: number
  only_profitable?: boolean
  only_with_funding?: boolean
}

export async function fetchSignals(filters: SignalFilters = {}): Promise<Signal[]> {
  const query = new URLSearchParams()
  Object.entries(filters).forEach(([k, v]) => {
    if (v == null || v === '' || v === false) return
    if (Array.isArray(v)) v.forEach((value) => query.append(k, String(value)))
    else query.set(k, String(v))
  })
  const res = await fetch(`${API_BASE}/signals?${query.toString()}`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to fetch signals')
  return res.json()
}

export async function fetchFundingMonitor(): Promise<FundingMonitorRow[]> {
  const res = await fetch(`${API_BASE}/funding/monitor`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to fetch funding monitor')
  return res.json()
}
