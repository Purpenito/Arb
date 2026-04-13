from datetime import datetime, timezone

from app.core.symbols import canonical_symbol
from app.core.types import FundingSnapshot, TopOfBook
from app.exchange_adapters.http_base import RestPollingAdapter


class BingXAdapter(RestPollingAdapter):
    name = "bingx"
    instruments_url = "https://open-api.bingx.com/openApi/swap/v2/quote/contracts"
    ticker_url = "https://open-api.bingx.com/openApi/swap/v2/quote/ticker"

    async def fetch_instruments(self):
        data = await self._get_json(self.instruments_url)
        out = []
        for i in data.get("data", []):
            base, quote = i["symbol"].split("-")[:2]
            out.append(self._to_instrument(native_symbol=i["symbol"], base=base, quote=quote, settle=quote))
        return out

    async def fetch_top_of_book_snapshot(self) -> list[TopOfBook]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in data.get("data", []):
            base, quote = i["symbol"].split("-")[:2]
            out.append(
                self._to_tob(
                    canonical=canonical_symbol(base, quote, quote),
                    bid=i.get("bidPrice", "0"),
                    ask=i.get("askPrice", "0"),
                    bid_size=i.get("bidQty", "0"),
                    ask_size=i.get("askQty", "0"),
                    mark=i.get("markPrice"),
                )
            )
        return out

    async def fetch_current_funding(self) -> list[FundingSnapshot]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in data.get("data", []):
            base, quote = i["symbol"].split("-")[:2]
            next_ts = i.get("nextFundingTime")
            next_time = datetime.fromtimestamp(int(next_ts) / 1000, tz=timezone.utc) if next_ts else None
            out.append(
                self._to_funding(
                    canonical=canonical_symbol(base, quote, quote),
                    rate=i.get("fundingRate", "0"),
                    mark_price=i.get("markPrice"),
                    next_funding_time=next_time,
                    interval_minutes=480,
                )
            )
        return out
