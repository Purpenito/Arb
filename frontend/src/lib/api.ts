import { Signal } from '@/types/signal'

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? 'http://localhost:8000/api/v1'

export async function fetchSignals(): Promise<Signal[]> {
  const res = await fetch(`${API_BASE}/signals`, { cache: 'no-store' })
  if (!res.ok) throw new Error('Failed to fetch signals')
  return res.json()
}
