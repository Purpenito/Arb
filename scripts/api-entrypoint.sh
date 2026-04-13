#!/usr/bin/env sh
set -eu

MAX_RETRIES="${MIGRATION_MAX_RETRIES:-30}"
SLEEP_SECONDS="${MIGRATION_RETRY_SLEEP_SECONDS:-2}"

attempt=1
while [ "$attempt" -le "$MAX_RETRIES" ]; do
  echo "[entrypoint] Running Alembic migrations (attempt ${attempt}/${MAX_RETRIES})..."
  if alembic upgrade head; then
    echo "[entrypoint] Migrations applied successfully."
    break
  fi
  if [ "$attempt" -eq "$MAX_RETRIES" ]; then
    echo "[entrypoint] Migration failed after ${MAX_RETRIES} attempts." >&2
    exit 1
  fi
  attempt=$((attempt + 1))
  sleep "$SLEEP_SECONDS"
done

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
