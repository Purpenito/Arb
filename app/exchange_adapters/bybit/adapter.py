from datetime import datetime, timezone

from app.core.symbols import canonical_symbol
from app.core.types import FundingSnapshot, TopOfBook
from app.exchange_adapters.http_base import RestPollingAdapter


class BybitAdapter(RestPollingAdapter):
    name = "bybit"
    instruments_url = "https://api.bybit.com/v5/market/instruments-info?category=linear"
    ticker_url = "https://api.bybit.com/v5/market/tickers?category=linear"

    async def fetch_instruments(self):
        data = await self._get_json(self.instruments_url)
        items = data.get("result", {}).get("list", [])
        out = []
        for i in items:
            out.append(
                self._to_instrument(
                    native_symbol=i["symbol"],
                    base=i["baseCoin"],
                    quote=i["quoteCoin"],
                    settle=i.get("settleCoin", i["quoteCoin"]),
                    tick_size=i.get("priceFilter", {}).get("tickSize", "0.1"),
                    qty_step=i.get("lotSizeFilter", {}).get("qtyStep", "0.001"),
                    min_qty=i.get("lotSizeFilter", {}).get("minOrderQty", "0.001"),
                )
            )
        return out

    async def fetch_top_of_book_snapshot(self) -> list[TopOfBook]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in data.get("result", {}).get("list", []):
            canonical = canonical_symbol(i.get("symbol", "").replace("USDT", ""), "USDT", "USDT")
            out.append(
                self._to_tob(
                    canonical=canonical,
                    bid=i.get("bid1Price", "0"),
                    ask=i.get("ask1Price", "0"),
                    bid_size=i.get("bid1Size", "0"),
                    ask_size=i.get("ask1Size", "0"),
                    mark=i.get("markPrice"),
                    index=i.get("indexPrice"),
                )
            )
        return out

    async def fetch_current_funding(self) -> list[FundingSnapshot]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in data.get("result", {}).get("list", []):
            canonical = canonical_symbol(i.get("symbol", "").replace("USDT", ""), "USDT", "USDT")
            ts = i.get("nextFundingTime")
            next_time = datetime.fromtimestamp(int(ts) / 1000, tz=timezone.utc) if ts else None
            out.append(
                self._to_funding(
                    canonical=canonical,
                    rate=i.get("fundingRate", "0"),
                    mark_price=i.get("markPrice"),
                    next_funding_time=next_time,
                    interval_minutes=480,
                )
            )
        return out
