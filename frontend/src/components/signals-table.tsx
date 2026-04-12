'use client'

import { Signal } from '@/types/signal'

const sortableKeys = ['net_profit_pct', 'net_funding_edge_pct', 'estimated_pnl_usdt', 'max_executable_size_usdt', 'liquidity_score', 'symbol', 'updated_at'] as const

type SortKey = (typeof sortableKeys)[number]

export function SignalsTable({ signals, onSelect, sortKey, setSortKey }: { signals: Signal[]; onSelect: (s: Signal) => void; sortKey: SortKey; setSortKey: (k: SortKey) => void }) {
  const sorted = [...signals].sort((a, b) => {
    const va = (a[sortKey] ?? -Infinity) as number | string
    const vb = (b[sortKey] ?? -Infinity) as number | string
    return va > vb ? -1 : 1
  })

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th onClick={() => setSortKey('symbol')}>Symbol</th>
            <th>Arbitrage Type</th>
            <th>Exchange Long / Buy</th>
            <th>Exchange Short / Sell</th>
            <th>Long price</th>
            <th>Short price</th>
            <th>Spread %</th>
            <th>Fees %</th>
            <th onClick={() => setSortKey('net_profit_pct')}>Net profit %</th>
            <th onClick={() => setSortKey('net_funding_edge_pct')}>Funding edge %</th>
            <th onClick={() => setSortKey('max_executable_size_usdt')}>Executable size</th>
            <th onClick={() => setSortKey('estimated_pnl_usdt')}>Estimated PnL</th>
            <th onClick={() => setSortKey('liquidity_score')}>Liquidity</th>
            <th onClick={() => setSortKey('updated_at')}>Updated at</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((s) => (
            <tr key={s.signal_id} onClick={() => onSelect(s)}>
              <td>{s.symbol}</td>
              <td>{s.arbitrage_type}</td>
              <td>{s.buy_or_long.exchange}</td>
              <td>{s.sell_or_short.exchange}</td>
              <td>{s.buy_or_long.price.toFixed(2)}</td>
              <td>{s.sell_or_short.price.toFixed(2)}</td>
              <td>{s.gross_spread_pct.toFixed(3)}</td>
              <td>{s.total_fees_pct.toFixed(3)}</td>
              <td className={s.net_profit_pct >= 0 ? 'pos' : 'neg'}>{s.net_profit_pct.toFixed(3)}</td>
              <td className={(s.net_funding_edge_pct ?? 0) >= 0 ? 'pos' : 'neg'}>{s.net_funding_edge_pct?.toFixed(3) ?? '—'}</td>
              <td>{s.max_executable_size_usdt.toLocaleString()}</td>
              <td>{s.estimated_pnl_usdt.toFixed(2)}</td>
              <td>{s.liquidity_score.toFixed(2)}</td>
              <td>{new Date(s.updated_at).toLocaleTimeString()}</td>
              <td><a href={s.buy_or_long.link} onClick={(e) => e.stopPropagation()} target="_blank">Open</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
