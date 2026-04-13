from datetime import datetime, timezone

from app.core.symbols import canonical_symbol
from app.core.types import FundingSnapshot, TopOfBook
from app.exchange_adapters.http_base import RestPollingAdapter


class OKXAdapter(RestPollingAdapter):
    name = "okx"
    instruments_url = "https://www.okx.com/api/v5/public/instruments?instType=SWAP"
    ticker_url = "https://www.okx.com/api/v5/market/tickers?instType=SWAP"
    funding_url = "https://www.okx.com/api/v5/public/funding-rate?instId={inst_id}"

    async def fetch_instruments(self):
        data = await self._get_json(self.instruments_url)
        out = []
        for i in data.get("data", []):
            base, quote, settle = i.get("instId", "--").split("-")[:3]
            out.append(
                self._to_instrument(
                    native_symbol=i["instId"],
                    base=base,
                    quote=quote,
                    settle=settle,
                    tick_size=i.get("tickSz", "0.1"),
                    qty_step=i.get("lotSz", "0.001"),
                    min_qty=i.get("minSz", "0.001"),
                )
            )
        return out

    async def fetch_top_of_book_snapshot(self) -> list[TopOfBook]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in data.get("data", []):
            base, quote, settle = i.get("instId", "--").split("-")[:3]
            out.append(
                self._to_tob(
                    canonical=canonical_symbol(base, quote, settle),
                    bid=i.get("bidPx", "0"),
                    ask=i.get("askPx", "0"),
                    bid_size=i.get("bidSz", "0"),
                    ask_size=i.get("askSz", "0"),
                    mark=i.get("last"),
                )
            )
        return out

    async def fetch_current_funding(self) -> list[FundingSnapshot]:
        ticks = await self._get_json(self.ticker_url)
        out = []
        for i in ticks.get("data", []):
            inst = i.get("instId")
            fund = await self._get_json(self.funding_url.format(inst_id=inst))
            f = (fund.get("data") or [{}])[0]
            base, quote, settle = inst.split("-")[:3]
            next_time = (
                datetime.fromtimestamp(int(f["nextFundingTime"]) / 1000, tz=timezone.utc)
                if f.get("nextFundingTime")
                else None
            )
            out.append(
                self._to_funding(
                    canonical=canonical_symbol(base, quote, settle),
                    rate=f.get("fundingRate", "0"),
                    mark_price=i.get("last"),
                    next_funding_time=next_time,
                    interval_minutes=480,
                )
            )
        return out
