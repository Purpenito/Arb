from datetime import datetime, timezone

from app.core.symbols import canonical_symbol
from app.core.types import FundingSnapshot, TopOfBook
from app.exchange_adapters.http_base import RestPollingAdapter


class KuCoinAdapter(RestPollingAdapter):
    name = "kucoin"
    instruments_url = "https://api-futures.kucoin.com/api/v1/contracts/active"
    ticker_url = "https://api-futures.kucoin.com/api/v1/allTickers"

    @staticmethod
    def _extract_contracts(data: dict) -> list[dict]:
        raw = data.get("data", [])
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            for key in ("contracts", "items", "list"):
                value = raw.get(key)
                if isinstance(value, list):
                    return value
        return []

    @staticmethod
    def _extract_tickers(data: dict) -> list[dict]:
        raw = data.get("data", [])
        if isinstance(raw, list):
            return raw
        if isinstance(raw, dict):
            ticker = raw.get("ticker")
            if isinstance(ticker, list):
                return ticker
            for key in ("items", "list"):
                value = raw.get(key)
                if isinstance(value, list):
                    return value
        return []

    async def fetch_instruments(self):
        data = await self._get_json(self.instruments_url)
        out = []
        for i in self._extract_contracts(data):
            out.append(
                self._to_instrument(
                    native_symbol=i.get("symbol", ""),
                    base=i.get("baseCurrency", ""),
                    quote=i.get("quoteCurrency", "USDT"),
                    settle=i.get("settleCurrency", "USDT"),
                    tick_size=i.get("tickSize", "0.1"),
                    qty_step=i.get("lotSize", "0.001"),
                    min_qty=i.get("multiplier", "0.001"),
                )
            )
        return out

    async def fetch_top_of_book_snapshot(self) -> list[TopOfBook]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in self._extract_tickers(data):
            symbol = i.get("symbol", "")
            base = symbol.replace("USDTM", "")
            out.append(
                self._to_tob(
                    canonical=canonical_symbol(base, "USDT", "USDT"),
                    bid=i.get("bestBidPrice", "0"),
                    ask=i.get("bestAskPrice", "0"),
                    bid_size=i.get("bestBidSize", "0"),
                    ask_size=i.get("bestAskSize", "0"),
                    mark=i.get("markPrice"),
                )
            )
        return out

    async def fetch_current_funding(self) -> list[FundingSnapshot]:
        data = await self._get_json(self.ticker_url)
        out = []
        for i in self._extract_tickers(data):
            symbol = i.get("symbol", "")
            base = symbol.replace("USDTM", "")
            next_ts = i.get("nextFundingRateTime")
            next_time = datetime.fromtimestamp(int(next_ts) / 1000, tz=timezone.utc) if next_ts else None
            out.append(
                self._to_funding(
                    canonical=canonical_symbol(base, "USDT", "USDT"),
                    rate=i.get("fundingFeeRate", "0"),
                    mark_price=i.get("markPrice"),
                    next_funding_time=next_time,
                    interval_minutes=480,
                )
            )
        return out
