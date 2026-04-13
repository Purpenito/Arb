from decimal import Decimal

from app.exchange_adapters.http_base import RestPollingAdapter


class DummyAdapter(RestPollingAdapter):
    name = "dummy"

    async def fetch_instruments(self):
        return []

    async def fetch_current_funding(self):
        return []

    async def fetch_funding_history(self, canonical_symbol: str, limit: int = 50):
        return []

    async def fetch_top_of_book_snapshot(self):
        return []

    async def ws_subscribe_top_of_book(self):
        return None


def test_invalid_funding_rate_is_safely_zero():
    ad = DummyAdapter()
    snap = ad._to_funding("BTC/USDT:USDT", rate="", mark_price="", next_funding_time=None, interval_minutes=480)
    assert snap.funding_rate == Decimal("0")
    assert snap.mark_price is None
