'use client'

import { useEffect, useMemo, useState } from 'react'

import { FiltersPanel } from '@/components/filters-panel'
import { SignalModal } from '@/components/signal-modal'
import { SignalsTable } from '@/components/signals-table'
import { fetchSignals } from '@/lib/api'
import { Signal } from '@/types/signal'

export default function HomePage() {
  const [signals, setSignals] = useState<Signal[]>([])
  const [selected, setSelected] = useState<Signal | null>(null)
  const [search, setSearch] = useState('')
  const [minNet, setMinNet] = useState(0)
  const [onlyFunding, setOnlyFunding] = useState(false)
  const [sortKey, setSortKey] = useState<'net_profit_pct' | 'net_funding_edge_pct' | 'estimated_pnl_usdt' | 'max_executable_size_usdt' | 'liquidity_score' | 'symbol' | 'updated_at'>('net_profit_pct')

  useEffect(() => {
    fetchSignals().then(setSignals)
    const ws = new WebSocket((process.env.NEXT_PUBLIC_WS_BASE ?? 'ws://localhost:8000') + '/ws/signals')
    ws.onopen = () => ws.send('subscribe')
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data)
      if (msg.type === 'signals') setSignals(msg.data)
    }
    return () => ws.close()
  }, [])

  const filtered = useMemo(
    () => signals.filter((s) => s.symbol.includes(search) && s.net_profit_pct >= minNet && (!onlyFunding || s.net_funding_edge_pct != null)),
    [signals, search, minNet, onlyFunding],
  )

  return (
    <main className="layout">
      <FiltersPanel
        search={search}
        onSearch={setSearch}
        minNet={minNet}
        onMinNet={setMinNet}
        onlyFunding={onlyFunding}
        onOnlyFunding={setOnlyFunding}
      />
      <SignalsTable signals={filtered} onSelect={setSelected} sortKey={sortKey} setSortKey={setSortKey} />
      {selected && <SignalModal signal={selected} onClose={() => setSelected(null)} />}
    </main>
  )
}
