import { HealthResponse, SystemStatus } from '@/lib/types';

export function SystemHealth({ health, status }: { health: HealthResponse; status: SystemStatus }) {
  return (
    <div className="card">
      <h2>System Health</h2>
      <p>
        API: <span className={health.status === 'ok' ? 'pill-ok' : 'pill-warn'}>{health.status}</span> | DB: {health.db} | Redis: {health.redis}
      </p>
      <p>
        Collector: <span className={status.collector === 'running' ? 'pill-ok' : 'pill-warn'}>{status.collector}</span>
      </p>
      <ul>
        {Object.entries(status.adapters).map(([k, v]) => (
          <li key={k}>{k}: <span className={v === 'ok' ? 'pill-ok' : 'pill-warn'}>{v}</span></li>
        ))}
      </ul>
    </div>
  );
}
