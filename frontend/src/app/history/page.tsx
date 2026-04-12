export default async function HistoryPage() {
  const res = await fetch('http://localhost:8000/api/v1/history/analytics', { cache: 'no-store' })
  const data = await res.json()

  return (
    <main style={{ padding: 20 }}>
      <h1>Analytics / History</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </main>
  )
}
