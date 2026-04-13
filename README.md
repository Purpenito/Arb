# Arb Scanner Platform (Read-Only, No Execution)

Production-oriented **fullstack** scanner for crypto derivatives arbitrage surveillance:
- Futures-Futures arbitrage
- Funding monitor
- Funding arbitrage

Exchanges in v1: **Bybit, OKX, KuCoin, BingX, Gate**.

> v1 is strictly read-only: no order execution/trading actions are implemented.

## Stack

- **Backend**: Python 3.12+, FastAPI, asyncio, aiohttp, SQLAlchemy 2.0, Alembic
- **Frontend**: Next.js (App Router), TypeScript, reusable component tables/cards
- **Data**: PostgreSQL, Redis
- **Ops**: Docker, Docker Compose, structured JSON logs

## Architecture

```
frontend (Next.js dashboard)
      |
      v
backend api (FastAPI) <---- redis (health/cache/event-ready)
      |
      v
collectors + arb engine
      |
      v
postgres (normalized market/funding/opportunities)
```

### Backend modules

- `app/exchange_adapters/`: pluggable adapters (Bybit/OKX/KuCoin/BingX/Gate)
- `app/core/`: canonical symbols, compatibility, math formulas, freshness
- `app/storage/`: SQLAlchemy models + db session
- `app/repositories/`: persistence methods
- `app/services/`: collectors, health state, arbitrage engine
- `app/api/`: typed endpoints for dashboard
- `app/infra/`: settings + logging

### Frontend modules

- `frontend/app/`: app layout/page
- `frontend/components/`: reusable cards/tables/system health widgets
- `frontend/lib/`: typed API client + TS response types

## Core formulas

- Futures spread (ask/bid executable):
  - `gross_spread_pct = (sell_bid / buy_ask - 1) * 100`
  - `net_spread_pct = gross_spread_pct - fee_estimate_pct - slippage_estimate_pct - execution_buffer_pct`

- Funding arb:
  - `net_expected_pct = funding_receive_pct - funding_pay_pct - fee_estimate_pct - slippage_estimate_pct - basis_risk_buffer_pct`

## API endpoints

- `GET /health`
- `GET /system/status`
- `GET /exchanges`
- `GET /instruments`
- `GET /opportunities/futures-futures`
- `GET /funding/current`
- `GET /funding/history`
- `GET /opportunities/funding`

## Quickstart

```bash
cp .env.example .env
docker compose up --build
```

- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000
- API container now auto-runs `alembic upgrade head` on startup (with retries) before launching Uvicorn.

## Local dev

### Backend

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```



## Troubleshooting

- If Alembic receives `DATABASE_URL` as `postgresql+asyncpg://`, `postgresql://`, or `postgres://`, this repo auto-normalizes it to `postgresql+psycopg://` for sync migrations in `alembic/env.py` (prevents `MissingGreenlet` and missing `psycopg2` issues).
- Re-run manually (if needed): `docker compose run --rm api alembic upgrade head`.

## Migration note

- `0001` is the historical bootstrap migration.
- `0002_create_missing_core_tables` is an idempotent schema-completion migration that creates all required core tables if they are missing (useful when old environments were migrated with only `exchanges`).
- Run `alembic upgrade head` after pulling updates.

## Testing

```bash
pytest -q
```

## Add a new exchange

1. Implement adapter class under `app/exchange_adapters/<new>/adapter.py`
2. Conform to `ExchangeAdapter` interface
3. Normalize to canonical symbol `BASE/QUOTE:SETTLE`
4. Register in `app/exchange_adapters/__init__.py`
5. Add parser/integration tests

## Assumptions

- REST polling is baseline ingestion; websocket hooks are available in adapter interfaces.
- Top-of-book notional is used as conservative tradable-size estimate.
- Some exchange endpoints differ by product type; parsers keep fallback guards.

## Known limitations

- Alembic migration is intentionally bootstrap-level and should be expanded for full production schema evolution.
- Funding history ingestion schedule is adapter-specific and can be expanded by a dedicated background service.
- Exchange-level per-symbol fee tiers are not yet modeled (uses exchange-level defaults currently).

## Next production improvements

- Dedicated websocket ingestion workers and snapshot-delta reconciliation.
- Redis streams for decoupled ingest/compute fan-out.
- Prometheus metrics + OpenTelemetry traces + alerting integrations.
- Materialized views / optimized DB indexes for high-cardinality symbols.
