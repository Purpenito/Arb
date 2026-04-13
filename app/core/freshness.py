from datetime import datetime, timezone


def is_stale(ts: datetime, threshold_ms: int) -> bool:
    now = datetime.now(timezone.utc)
    age_ms = (now - ts).total_seconds() * 1000
    return age_ms > threshold_ms
