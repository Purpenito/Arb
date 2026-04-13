from app.core.symbols import canonical_symbol
from app.core.types import FundingSnapshot, TopOfBook
from app.exchange_adapters.http_base import RestPollingAdapter


class GateAdapter(RestPollingAdapter):
    name = "gate"
    instruments_url = "https://api.gateio.ws/api/v4/futures/usdt/contracts"
    ticker_url = "https://api.gateio.ws/api/v4/futures/usdt/tickers"

    async def fetch_instruments(self):
        data = await self._get_json(self.instruments_url)
        out = []
        for i in data:
            base = i["name"].replace("_USDT", "")
            out.append(self._to_instrument(native_symbol=i["name"], base=base, quote="USDT", settle="USDT"))
        return out

    async def fetch_top_of_book_snapshot(self) -> list[TopOfBook]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in data:
            base = i["contract"].replace("_USDT", "")
            out.append(
                self._to_tob(
                    canonical=canonical_symbol(base, "USDT", "USDT"),
                    bid=i.get("highest_bid", "0"),
                    ask=i.get("lowest_ask", "0"),
                    bid_size=i.get("highest_size", "0"),
                    ask_size=i.get("lowest_size", "0"),
                    mark=i.get("mark_price"),
                )
            )
        return out

    async def fetch_current_funding(self) -> list[FundingSnapshot]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in data:
            base = i["contract"].replace("_USDT", "")
            out.append(
                self._to_funding(
                    canonical=canonical_symbol(base, "USDT", "USDT"),
                    rate=i.get("funding_rate", "0"),
                    mark_price=i.get("mark_price"),
                    next_funding_time=None,
                    interval_minutes=480,
                )
            )
        return out
