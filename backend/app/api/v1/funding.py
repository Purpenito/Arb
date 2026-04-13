from fastapi import APIRouter

from app.adapters.mock import ADAPTERS

router = APIRouter(prefix='/funding', tags=['funding'])


@router.get('/monitor')
async def funding_monitor():
    symbols = await ADAPTERS[0].fetch_symbols()
    payload = []
    for symbol in symbols:
        rows = []
        for adapter in ADAPTERS:
            snapshot = await adapter.fetch_funding(symbol)
            if snapshot:
                rows.append({'exchange': adapter.name, 'funding_rate_pct': round(snapshot.funding_rate_pct, 4)})
        if rows:
            values = [r['funding_rate_pct'] for r in rows]
            payload.append({
                'symbol': symbol,
                'rates': rows,
                'max_funding_spread_pct': round(max(values) - min(values), 4),
            })
    return payload
