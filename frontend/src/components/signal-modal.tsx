'use client'

import { Signal } from '@/types/signal'

export function SignalModal({ signal, onClose }: { signal: Signal; onClose: () => void }) {
  const fundingLine = signal.net_funding_edge_pct == null
    ? 'Funding is not part of this setup.'
    : signal.net_funding_edge_pct >= 0
      ? 'Positive edge: SHORT side gets relative funding advantage.'
      : 'Negative edge: LONG side gets relative funding advantage.'

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()}>
        <h2>{signal.symbol} — {signal.arbitrage_type}</h2>
        <p>{signal.buy_or_long.side} @ {signal.buy_or_long.exchange}: {signal.buy_or_long.price.toFixed(6)}</p>
        <p>{signal.sell_or_short.side} @ {signal.sell_or_short.exchange}: {signal.sell_or_short.price.toFixed(6)}</p>
        <p>Spread: {signal.gross_spread_pct.toFixed(4)}% · Fees: {signal.total_fees_pct.toFixed(4)}% · Net: {signal.net_profit_pct.toFixed(4)}%</p>
        <p>Funding edge: {signal.net_funding_edge_pct?.toFixed(4) ?? '—'}% — {fundingLine}</p>
        <p>Max executable size: {signal.max_executable_size_usdt.toLocaleString()} USDT · Estimated PnL: {signal.estimated_pnl_usdt.toFixed(2)} USDT</p>
        <p>Lifetime: {Math.floor(signal.signal_lifetime_sec / 60)} minutes · Updated at {new Date(signal.updated_at).toLocaleString()}</p>
        <p>
          Open market: <a href={signal.buy_or_long.link} target="_blank">LONG/BUY ↗</a> · <a href={signal.sell_or_short.link} target="_blank">SHORT/SELL ↗</a>
        </p>
      </div>
    </div>
  )
}
