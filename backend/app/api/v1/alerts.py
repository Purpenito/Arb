from fastapi import APIRouter

from app.schemas.signal import AlertRule

router = APIRouter(prefix='/alerts', tags=['alerts'])

_ALERTS: dict[str, AlertRule] = {}


@router.get('')
async def list_alerts():
    return list(_ALERTS.values())


@router.post('')
async def create_alert(rule: AlertRule):
    _ALERTS[rule.id] = rule
    return rule
