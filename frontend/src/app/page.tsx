'use client'

import { useEffect, useMemo, useState } from 'react'
import Link from 'next/link'

import { DashboardFilters, FiltersPanel } from '@/components/filters-panel'
import { SignalModal } from '@/components/signal-modal'
import { SignalsTable } from '@/components/signals-table'
import { fetchSignals } from '@/lib/api'
import { Signal } from '@/types/signal'

const exchanges = ['Binance', 'Bybit', 'OKX', 'KuCoin', 'Bitget', 'BingX', 'MEXC', 'Gate', 'HTX']

export default function HomePage() {
  const [signals, setSignals] = useState<Signal[]>([])
  const [selected, setSelected] = useState<Signal | null>(null)
  const [sortKey, setSortKey] = useState<'symbol' | 'gross_spread_pct' | 'total_fees_pct' | 'net_profit_pct' | 'net_funding_edge_pct' | 'max_executable_size_usdt' | 'estimated_pnl_usdt' | 'liquidity_score' | 'updated_at' | 'signal_lifetime_sec'>('net_profit_pct')
  const [sortDir, setSortDir] = useState<'asc' | 'desc'>('desc')

  const [filters, setFilters] = useState<DashboardFilters>({
    search: '', longExchanges: [], shortExchanges: [], whitelistCoins: '', blacklistCoins: '',
    minVolume: 0, maxVolume: 2_000_000, minNet: -10, maxNet: 100, minFundingEdge: -100,
    arbitrageType: 'all', onlyProfitable: true, onlyFunding: false, refreshMs: 2000,
  })

  useEffect(() => {
    const load = () => fetchSignals({
      search: filters.search,
      arbitrage_types: filters.arbitrageType === 'all' ? [] : [filters.arbitrageType],
      long_exchanges: filters.longExchanges,
      short_exchanges: filters.shortExchanges,
      whitelist_coins: filters.whitelistCoins.split(',').map((s) => s.trim()).filter(Boolean),
      blacklist_coins: filters.blacklistCoins.split(',').map((s) => s.trim()).filter(Boolean),
      min_volume_usdt: filters.minVolume,
      max_volume_usdt: filters.maxVolume,
      min_net_profit_pct: filters.minNet,
      max_net_profit_pct: filters.maxNet,
      min_funding_edge_pct: filters.minFundingEdge,
      only_profitable: filters.onlyProfitable,
      only_with_funding: filters.onlyFunding,
    }).then(setSignals)

    load()
    const id = setInterval(load, filters.refreshMs)
    return () => clearInterval(id)
  }, [filters])

  const onSort = (key: typeof sortKey) => {
    if (sortKey === key) setSortDir((d) => d === 'asc' ? 'desc' : 'asc')
    else { setSortKey(key); setSortDir('desc') }
  }

  const topStats = useMemo(() => ({
    total: signals.length,
    profitable: signals.filter((s) => s.net_profit_pct > 0).length,
    funding: signals.filter((s) => s.net_funding_edge_pct != null).length,
  }), [signals])

  return (
    <main className="terminal-page">
      <header className="topbar">
        <h1>Спотовый скринер</h1>
        <nav><Link href="/">Сигналы</Link> · <Link href="/funding-monitor">Funding Monitor</Link> · <Link href="/history">История</Link></nav>
      </header>
      <section className="stats-row">
        <div className="stat">Total: <b>{topStats.total}</b></div>
        <div className="stat">Profitable: <b className="pos">{topStats.profitable}</b></div>
        <div className="stat">Funding Opps: <b>{topStats.funding}</b></div>
      </section>
      <FiltersPanel exchanges={exchanges} value={filters} onChange={(patch) => setFilters((prev) => ({ ...prev, ...patch }))} />
      <SignalsTable signals={signals} onSelect={setSelected} sortKey={sortKey} sortDir={sortDir} setSort={onSort} />
      {selected && <SignalModal signal={selected} onClose={() => setSelected(null)} />}
    </main>
  )
}
