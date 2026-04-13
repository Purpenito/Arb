import { FuturesOpportunity } from '@/lib/types';
import { TableCard } from './TableCard';

export function FuturesTable({ rows }: { rows: FuturesOpportunity[] }) {
  return (
    <TableCard title="Futures-Futures Opportunities">
      <table className="table">
        <thead><tr><th>Coin</th><th>Buy</th><th>Sell</th><th>Buy Ask</th><th>Sell Bid</th><th>Gross %</th><th>Net %</th><th>Size $</th><th>Freshness</th></tr></thead>
        <tbody>
          {rows.slice(0, 20).map((r, i) => (
            <tr key={`${r.canonical_symbol}-${i}`}>
              <td>{r.canonical_symbol}</td><td>{r.buy_exchange}</td><td>{r.sell_exchange}</td><td>{r.buy_ask}</td><td>{r.sell_bid}</td><td>{r.gross_spread_pct}</td><td>{r.net_spread_pct}</td><td>{r.max_tradable_notional}</td><td>{r.freshness_ms}ms</td>
            </tr>
          ))}
        </tbody>
      </table>
    </TableCard>
  );
}
