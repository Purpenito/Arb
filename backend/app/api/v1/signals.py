from fastapi import APIRouter

from app.schemas.signal import SignalFilter
from app.services.signal_service import SignalService

router = APIRouter(prefix='/signals', tags=['signals'])
service = SignalService()


@router.get('')
async def list_signals(
    search: str | None = None,
    min_net_profit_pct: float | None = None,
    min_funding_edge_pct: float | None = None,
    only_with_funding: bool = False,
):
    filters = SignalFilter(
        search=search,
        min_net_profit_pct=min_net_profit_pct,
        min_funding_edge_pct=min_funding_edge_pct,
        only_with_funding=only_with_funding,
    )
    return await service.get_signals(filters)
