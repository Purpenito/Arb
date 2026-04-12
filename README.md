# Crypto Arbitrage Monitor

Production-style foundation for a real-time crypto arbitrage platform with Next.js frontend + FastAPI backend.

## 1) Architecture plan

- **Ingestion layer**: exchange adapters normalize symbols, fees, top-of-book, funding.
- **Arbitrage engine**: computes Spot→Futures, Futures→Futures, and Funding arbitrage with LONG/SHORT semantics.
- **Serving layer**: REST endpoints for initial loads and WebSocket stream for live signal updates.
- **Persistence**: PostgreSQL for users/presets/history/alerts and Redis for hot market cache + pub/sub.
- **Client**: dark trader UI with large sortable table, fast filters, signal drill-down modal, and analytics page.

## 2) Project structure

```text
/backend
  /app
    /adapters
    /api/v1
    /core
    /engine
    /models
    /schemas
    /services
    /ws
/frontend
  /src/app
  /src/components
  /src/lib
  /src/types
/infra
  schema.sql
  docker-compose.prod.yml
  nginx.conf
```

## 3) Backend API design

- `GET /api/v1/signals` — returns current opportunities (supports core filters).
- `GET /api/v1/history/analytics` — aggregate history analytics (MVP stub).
- `GET/POST /api/v1/alerts` — list and create alert rules.
- `WS /ws/signals` — live push stream of signal snapshots.

## 4) Exchange adapter interface

Each adapter implements:
- `fetch_symbols()`
- `fetch_top_of_book(symbol)`
- `fetch_funding(symbol)`
- `build_trading_link(symbol, market_type)`
- `normalize_symbol(symbol)`

## 5) Arbitrage logic covered

- **Spread**: gross spread %, total fees %, net spread %, estimated PnL USDT.
- **Funding**: `net_funding_edge = funding_short - funding_long`; positive funding means LONG pays SHORT, negative means SHORT pays LONG.
- **Executable size**: `min(liquidity_long_side, liquidity_short_side)` at top-of-book.

## 6) MVP implementation plan

1. Adapter abstraction + first exchanges.
2. Engine for 3 arbitrage classes.
3. REST + WS delivery.
4. Signal table with sorting/filtering + modal details.
5. Alerts UI/API and channels.
6. History analytics and durable storage.

## Local run

Backend:
```bash
cd backend
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

## Production install on a server (Docker + Nginx)

### 1. Prepare VM

```bash
sudo apt update && sudo apt -y upgrade
sudo apt -y install docker.io docker-compose-plugin git
sudo usermod -aG docker $USER
newgrp docker
```

### 2. Clone and configure

```bash
git clone <your_repo_url> arb-monitor
cd arb-monitor
cp infra/.env.prod.example infra/.env.prod
```

Set a strong password in `infra/.env.prod`:

```env
POSTGRES_PASSWORD=replace_with_strong_password
```

### 3. Start services

```bash
docker compose --env-file infra/.env.prod -f infra/docker-compose.prod.yml up -d --build
```

### 4. Apply DB schema

```bash
docker compose --env-file infra/.env.prod -f infra/docker-compose.prod.yml exec -T postgres \
  psql -U arb -d arb < infra/schema.sql
```

### 5. Verify

```bash
docker compose --env-file infra/.env.prod -f infra/docker-compose.prod.yml ps
curl -i http://<server_ip>/healthz
curl -i http://<server_ip>/api/v1/signals
```

### 6. Optional HTTPS with Cloudflare/Nginx Proxy Manager/Caddy

For quick production hardening, put TLS termination in front of port `80` and keep backend/frontend private in Docker network.
