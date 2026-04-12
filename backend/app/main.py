from contextlib import asynccontextmanager
import asyncio

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.api.v1.alerts import router as alerts_router
from app.api.v1.history import router as history_router
from app.api.v1.signals import router as signals_router, service
from app.core.config import settings
from app.ws.manager import ConnectionManager

manager = ConnectionManager()


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(_broadcast_loop())
    yield
    task.cancel()


app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(signals_router, prefix='/api/v1')
app.include_router(history_router, prefix='/api/v1')
app.include_router(alerts_router, prefix='/api/v1')


@app.get('/healthz')
async def healthz():
    return {'ok': True}


@app.websocket('/ws/signals')
async def signals_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def _broadcast_loop():
    while True:
        signals = await service.get_signals()
        await manager.broadcast_json({'type': 'signals', 'data': [s.model_dump() for s in signals]})
        await asyncio.sleep(settings.websocket_tick_ms / 1000)
