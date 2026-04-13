'use client'

import { Signal } from '@/types/signal'

type SortKey = 'symbol' | 'gross_spread_pct' | 'total_fees_pct' | 'net_profit_pct' | 'net_funding_edge_pct' | 'max_executable_size_usdt' | 'estimated_pnl_usdt' | 'liquidity_score' | 'updated_at' | 'signal_lifetime_sec'

function sparkline(data: number[]) {
  const bars = '▁▂▃▄▅▆▇█'
  const min = Math.min(...data)
  const max = Math.max(...data)
  return data.map((v) => bars[Math.min(7, Math.floor(((v - min) / ((max - min) || 1)) * 7))]).join('')
}

export function SignalsTable({ signals, onSelect, sortKey, sortDir, setSort }: { signals: Signal[]; onSelect: (s: Signal) => void; sortKey: SortKey; sortDir: 'asc' | 'desc'; setSort: (k: SortKey) => void }) {
  const sorted = [...signals].sort((a, b) => {
    const av = a[sortKey] as number | string
    const bv = b[sortKey] as number | string
    const result = av > bv ? 1 : av < bv ? -1 : 0
    return sortDir === 'asc' ? result : -result
  })

  const hs = (key: SortKey, label: string) => <th onClick={() => setSort(key)}>{label}</th>

  return (
    <div className="table-wrap terminal">
      <table>
        <thead>
          <tr>
            {hs('symbol', 'Ticker')}
            <th>Type</th>
            <th>LONG / BUY</th>
            <th>SHORT / SELL</th>
            <th>Entry Prices</th>
            {hs('gross_spread_pct', 'Spread %')}
            {hs('total_fees_pct', 'Fees %')}
            {hs('net_profit_pct', 'Net Profit %')}
            {hs('net_funding_edge_pct', 'Funding Edge %')}
            {hs('max_executable_size_usdt', 'Exec Size USDT')}
            {hs('estimated_pnl_usdt', 'Estimated PnL')}
            {hs('liquidity_score', 'Liquidity')}
            {hs('updated_at', 'Updated')}
            <th>Spread History</th>
            {hs('signal_lifetime_sec', 'Lifetime')}
            <th className="sticky-right">Биржи</th>
          </tr>
        </thead>
        <tbody>
          {sorted.map((s) => (
            <tr key={s.signal_id} onClick={() => onSelect(s)}>
              <td><span className="coin">{s.symbol[0]}</span>{s.symbol}</td>
              <td><span className="tag">{s.arbitrage_type}</span></td>
              <td>{s.buy_or_long.exchange}</td>
              <td>{s.sell_or_short.exchange}</td>
              <td>{s.buy_or_long.price.toFixed(4)} / {s.sell_or_short.price.toFixed(4)}</td>
              <td>{s.gross_spread_pct.toFixed(3)}</td>
              <td>{s.total_fees_pct.toFixed(3)}</td>
              <td className={s.net_profit_pct >= 0 ? 'pos strong' : 'neg strong'}>{s.net_profit_pct.toFixed(3)}</td>
              <td className={(s.net_funding_edge_pct ?? 0) >= 0 ? 'pos' : 'neg'}>{s.net_funding_edge_pct?.toFixed(3) ?? '—'}</td>
              <td>{s.max_executable_size_usdt.toLocaleString()}</td>
              <td className={s.estimated_pnl_usdt >= 0 ? 'pos' : 'neg'}>{s.estimated_pnl_usdt.toFixed(2)}</td>
              <td>{s.liquidity_score.toFixed(2)}</td>
              <td>{new Date(s.updated_at).toLocaleTimeString()}</td>
              <td className="mono">{sparkline(s.spread_history_pct)}</td>
              <td>{Math.floor(s.signal_lifetime_sec / 60)}m</td>
              <td className="sticky-right links"><a href={s.buy_or_long.link} onClick={(e) => e.stopPropagation()} target="_blank">{s.buy_or_long.exchange} ↗</a><a href={s.sell_or_short.link} onClick={(e) => e.stopPropagation()} target="_blank">{s.sell_or_short.exchange} ↗</a></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
