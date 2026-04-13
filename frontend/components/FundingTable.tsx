import { FundingCurrent, FundingOpportunity } from '@/lib/types';
import { TableCard } from './TableCard';

export function FundingTable({ current, opps }: { current: FundingCurrent[]; opps: FundingOpportunity[] }) {
  return (
    <>
      <TableCard title="Funding Monitor">
        <table className="table">
          <thead><tr><th>Coin</th><th>Exchange</th><th>Funding %</th><th>Annualized %</th><th>Next</th><th>Mark</th></tr></thead>
          <tbody>{current.slice(0, 20).map((r, i) => <tr key={`${r.exchange}-${r.canonical_symbol}-${i}`}><td>{r.canonical_symbol}</td><td>{r.exchange}</td><td>{r.funding_rate}</td><td>{r.annualized_funding_pct ?? '-'}</td><td>{r.next_funding_time ?? '-'}</td><td>{r.mark_price ?? '-'}</td></tr>)}</tbody>
        </table>
      </TableCard>
      <TableCard title="Funding Arbitrage Opportunities">
        <table className="table">
          <thead><tr><th>Coin</th><th>Receive On</th><th>Hedge On</th><th>Receive %</th><th>Pay %</th><th>Net %</th><th>Next</th></tr></thead>
          <tbody>{opps.slice(0, 20).map((r, i) => <tr key={`${r.canonical_symbol}-${i}`}><td>{r.canonical_symbol}</td><td>{r.receive_exchange}</td><td>{r.hedge_exchange}</td><td>{r.funding_receive_pct}</td><td>{r.funding_pay_pct}</td><td>{r.net_expected_pct}</td><td>{r.next_funding_time ?? '-'}</td></tr>)}</tbody>
        </table>
      </TableCard>
    </>
  );
}
