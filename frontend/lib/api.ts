import { FundingCurrent, FundingOpportunity, FuturesOpportunity, HealthResponse, SystemStatus } from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? 'http://localhost:8000';

async function getJson<T>(path: string): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, { cache: 'no-store' });
  if (!res.ok) throw new Error(`Failed ${path}`);
  return res.json() as Promise<T>;
}

export const api = {
  health: () => getJson<HealthResponse>('/health'),
  futures: () => getJson<FuturesOpportunity[]>('/opportunities/futures-futures'),
  fundingCurrent: () => getJson<FundingCurrent[]>('/funding/current'),
  fundingOpps: () => getJson<FundingOpportunity[]>('/opportunities/funding'),
  status: () => getJson<SystemStatus>('/system/status'),
};
