from fastapi import APIRouter, Query

from app.models.enums import ArbitrageType
from app.schemas.signal import SignalFilter
from app.services.signal_service import SignalService

router = APIRouter(prefix='/signals', tags=['signals'])
service = SignalService()


@router.get('')
async def list_signals(
    search: str | None = None,
    arbitrage_types: list[ArbitrageType] = Query(default=[]),
    long_exchanges: list[str] = Query(default=[]),
    short_exchanges: list[str] = Query(default=[]),
    whitelist_coins: list[str] = Query(default=[]),
    blacklist_coins: list[str] = Query(default=[]),
    min_volume_usdt: float | None = None,
    max_volume_usdt: float | None = None,
    min_net_profit_pct: float | None = None,
    max_net_profit_pct: float | None = None,
    min_funding_edge_pct: float | None = None,
    only_profitable: bool = False,
    only_with_funding: bool = False,
):
    filters = SignalFilter(
        search=search,
        arbitrage_types=arbitrage_types,
        long_exchanges=long_exchanges,
        short_exchanges=short_exchanges,
        whitelist_coins=[coin.upper() for coin in whitelist_coins],
        blacklist_coins=[coin.upper() for coin in blacklist_coins],
        min_volume_usdt=min_volume_usdt,
        max_volume_usdt=max_volume_usdt,
        min_net_profit_pct=min_net_profit_pct,
        max_net_profit_pct=max_net_profit_pct,
        min_funding_edge_pct=min_funding_edge_pct,
        only_profitable=only_profitable,
        only_with_funding=only_with_funding,
    )
    return await service.get_signals(filters)
