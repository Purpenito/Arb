from fastapi import APIRouter

router = APIRouter(prefix='/history', tags=['history'])


@router.get('/analytics')
async def analytics_stub():
    return {
        'top_symbols': [{'symbol': 'BTCUSDT', 'avg_pnl_usdt': 102.3}],
        'top_exchanges': [{'exchange': 'Binance', 'count': 42}],
        'longest_lasting': [{'symbol': 'ETHUSDT', 'seconds': 540}],
    }
