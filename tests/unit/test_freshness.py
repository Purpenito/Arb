from datetime import datetime, timedelta, timezone
from app.core.freshness import is_stale


def test_stale_filter():
    old = datetime.now(timezone.utc) - timedelta(seconds=10)
    assert is_stale(old, 3000)
