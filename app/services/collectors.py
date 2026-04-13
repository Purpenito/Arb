import asyncio
import logging
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession

from app.exchange_adapters import build_adapters
from app.infra.config import get_settings
from app.repositories.market_repository import MarketRepository
from app.services.arbitrage_engine import ArbitrageEngine
from app.services.state import runtime_state

logger = logging.getLogger(__name__)


async def with_retry(fn: Callable[[], Awaitable], attempts: int = 3, base_delay: float = 0.5):
    last_exc = None
    for i in range(attempts):
        try:
            return await fn()
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            await asyncio.sleep(base_delay * (2**i))
    if last_exc:
        raise last_exc


class CollectorOrchestrator:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.settings = get_settings()
        self.adapters = build_adapters()
        for ad in self.adapters:
            runtime_state.adapter_status[ad.name] = "unknown"

    async def run_once(self) -> None:
        runtime_state.collector_status = "running"
        runtime_state.updated_at = datetime.now(timezone.utc)
        async with self.session_factory() as session:  # type: AsyncSession
            repo = MarketRepository(session)
            for ad in self.adapters:
                try:
                    ex = await repo.upsert_exchange(ad.name)
                    instruments = await with_retry(ad.fetch_instruments)
                    for i in instruments:
                        await repo.upsert_instrument(ex.id, i)
                    quotes = await with_retry(ad.fetch_top_of_book_snapshot)
                    await repo.store_quotes(quotes)
                    funding = await with_retry(ad.fetch_current_funding)
                    await repo.store_funding(funding)
                    runtime_state.adapter_status[ad.name] = "ok"
                except Exception as exc:  # noqa: BLE001
                    runtime_state.adapter_status[ad.name] = "degraded"
                    logger.exception("collector_error", extra={"exchange": ad.name, "error": str(exc)})
            engine = ArbitrageEngine(session)
            await engine.compute()
            await session.commit()

    async def run_forever(self) -> None:
        while True:
            try:
                await self.run_once()
            except Exception:  # noqa: BLE001
                runtime_state.collector_status = "degraded"
                logger.exception("collector_run_once_failure")
            await asyncio.sleep(self.settings.collector_interval_seconds)
