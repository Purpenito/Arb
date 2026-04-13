import { FundingTable } from '@/components/FundingTable';
import { FuturesTable } from '@/components/FuturesTable';
import { SystemHealth } from '@/components/SystemHealth';
import { api } from '@/lib/api';

export default async function HomePage() {
  const [health, status, futures, fundingCurrent, fundingOpps] = await Promise.all([
    api.health(),
    api.status(),
    api.futures(),
    api.fundingCurrent(),
    api.fundingOpps(),
  ]);

  return (
    <div className="grid">
      <SystemHealth health={health} status={status} />
      <FuturesTable rows={futures} />
      <FundingTable current={fundingCurrent} opps={fundingOpps} />
    </div>
  );
}
