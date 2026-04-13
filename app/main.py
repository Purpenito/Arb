import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.routes import router
from app.infra.config import get_settings
from app.infra.logging import setup_logging
from app.services.collectors import CollectorOrchestrator
from app.storage.database import SessionLocal

collector_task: asyncio.Task | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global collector_task
    settings = get_settings()
    setup_logging(settings.log_level)
    orch = CollectorOrchestrator(SessionLocal)
    collector_task = asyncio.create_task(orch.run_forever())
    yield
    if collector_task:
        collector_task.cancel()


app = FastAPI(title="Arb Scanner", version="0.1.0", lifespan=lifespan)
app.include_router(router)
