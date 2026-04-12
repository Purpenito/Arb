'use client'

import { Signal } from '@/types/signal'

export function SignalModal({ signal, onClose }: { signal: Signal; onClose: () => void }) {
  const fundingHint = signal.net_funding_edge_pct != null
    ? signal.net_funding_edge_pct >= 0
      ? 'Funding advantage in favor of SHORT leg'
      : 'Funding advantage in favor of LONG leg'
    : 'No funding component for this signal'

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>{signal.symbol} — {signal.arbitrage_type}</h2>
        <p>{signal.buy_or_long.side} @ {signal.buy_or_long.exchange}: {signal.buy_or_long.price.toFixed(2)}</p>
        <p>{signal.sell_or_short.side} @ {signal.sell_or_short.exchange}: {signal.sell_or_short.price.toFixed(2)}</p>
        <p>Fees: {signal.total_fees_pct.toFixed(4)}%</p>
        <p>Net funding edge: {signal.net_funding_edge_pct?.toFixed(4) ?? '—'}%</p>
        <p>{fundingHint}</p>
        <p>Max executable size: {signal.max_executable_size_usdt.toLocaleString()} USDT</p>
        <p>Estimated PnL: {signal.estimated_pnl_usdt.toFixed(2)} USDT</p>
        <p>
          Links: <a href={signal.buy_or_long.link} target="_blank">Buy/Long</a> ·{' '}
          <a href={signal.sell_or_short.link} target="_blank">Sell/Short</a>
        </p>
        <p>
          Why signal appeared: price dislocation + fee/funding profile created {signal.net_profit_pct.toFixed(3)}% net edge
          with available liquidity of {signal.max_executable_size_usdt.toFixed(0)} USDT.
        </p>
      </div>
    </div>
  )
}
