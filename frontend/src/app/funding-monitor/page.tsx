import { fetchFundingMonitor } from '@/lib/api'

export default async function FundingMonitorPage() {
  const rows = await fetchFundingMonitor()
  const exchanges = Array.from(new Set(rows.flatMap((r) => r.rates.map((it) => it.exchange))))

  return (
    <main style={{ padding: 12 }}>
      <h1 style={{ margin: '0 0 12px' }}>Funding Monitor</h1>
      <div className="table-wrap terminal">
        <table>
          <thead>
            <tr>
              <th>Symbol</th>
              {exchanges.map((ex) => <th key={ex}>{ex}</th>)}
              <th>Max Funding Spread %</th>
            </tr>
          </thead>
          <tbody>
            {rows.sort((a, b) => b.max_funding_spread_pct - a.max_funding_spread_pct).map((row) => (
              <tr key={row.symbol}>
                <td>{row.symbol}</td>
                {exchanges.map((ex) => {
                  const rate = row.rates.find((r) => r.exchange === ex)?.funding_rate_pct
                  return <td key={`${row.symbol}-${ex}`} className={(rate ?? 0) >= 0 ? 'pos' : 'neg'}>{rate?.toFixed(4) ?? '—'}</td>
                })}
                <td className="strong">{row.max_funding_spread_pct.toFixed(4)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  )
}
