'use client'

import { ArbitrageType } from '@/types/signal'

export interface DashboardFilters {
  search: string
  longExchanges: string[]
  shortExchanges: string[]
  whitelistCoins: string
  blacklistCoins: string
  minVolume: number
  maxVolume: number
  minNet: number
  maxNet: number
  minFundingEdge: number
  arbitrageType: 'all' | ArbitrageType
  onlyProfitable: boolean
  onlyFunding: boolean
  refreshMs: number
}

interface Props {
  exchanges: string[]
  value: DashboardFilters
  onChange: (patch: Partial<DashboardFilters>) => void
}

export function FiltersPanel({ exchanges, value, onChange }: Props) {
  return (
    <section className="filters-top">
      <div className="filter-grid">
        <input placeholder="Search ticker" value={value.search} onChange={(e) => onChange({ search: e.target.value.toUpperCase() })} />
        <select value={value.arbitrageType} onChange={(e) => onChange({ arbitrageType: e.target.value as DashboardFilters['arbitrageType'] })}>
          <option value="all">All arbitrage types</option>
          <option value="spot_futures">Spot → Futures</option>
          <option value="futures_futures">Futures → Futures</option>
          <option value="funding">Funding monitor opportunities</option>
        </select>
        <input placeholder="Whitelist coins (BTC,ETH)" value={value.whitelistCoins} onChange={(e) => onChange({ whitelistCoins: e.target.value.toUpperCase() })} />
        <input placeholder="Blacklist coins (DOGE,PEPE)" value={value.blacklistCoins} onChange={(e) => onChange({ blacklistCoins: e.target.value.toUpperCase() })} />
        <input type="number" placeholder="Min size USDT" value={value.minVolume} onChange={(e) => onChange({ minVolume: Number(e.target.value) })} />
        <input type="number" placeholder="Max size USDT" value={value.maxVolume} onChange={(e) => onChange({ maxVolume: Number(e.target.value) })} />
        <input type="number" placeholder="Min net %" value={value.minNet} step="0.01" onChange={(e) => onChange({ minNet: Number(e.target.value) })} />
        <input type="number" placeholder="Max net %" value={value.maxNet} step="0.01" onChange={(e) => onChange({ maxNet: Number(e.target.value) })} />
        <input type="number" placeholder="Min funding edge %" value={value.minFundingEdge} step="0.001" onChange={(e) => onChange({ minFundingEdge: Number(e.target.value) })} />
        <select multiple value={value.longExchanges} onChange={(e) => onChange({ longExchanges: [...e.currentTarget.selectedOptions].map((o) => o.value) })}>
          {exchanges.map((exchange) => <option key={`l-${exchange}`}>{exchange}</option>)}
        </select>
        <select multiple value={value.shortExchanges} onChange={(e) => onChange({ shortExchanges: [...e.currentTarget.selectedOptions].map((o) => o.value) })}>
          {exchanges.map((exchange) => <option key={`s-${exchange}`}>{exchange}</option>)}
        </select>
        <select value={value.refreshMs} onChange={(e) => onChange({ refreshMs: Number(e.target.value) })}>
          <option value={1000}>Refresh 1s</option>
          <option value={2000}>Refresh 2s</option>
          <option value={5000}>Refresh 5s</option>
          <option value={10000}>Refresh 10s</option>
        </select>
      </div>
      <div className="toggle-row">
        <label><input type="checkbox" checked={value.onlyProfitable} onChange={(e) => onChange({ onlyProfitable: e.target.checked })} /> Only profitable</label>
        <label><input type="checkbox" checked={value.onlyFunding} onChange={(e) => onChange({ onlyFunding: e.target.checked })} /> Only funding opportunities</label>
        <button className="ghost">Advanced settings</button>
      </div>
    </section>
  )
}
