import asyncio

from app.exchange_adapters.bybit.adapter import BybitAdapter


def test_bybit_fetch_instruments_parsing():
    adapter = BybitAdapter()
    payload = {
        "result": {
            "list": [
                {
                    "symbol": "BTCUSDT",
                    "baseCoin": "BTC",
                    "quoteCoin": "USDT",
                    "settleCoin": "USDT",
                    "priceFilter": {"tickSize": "0.1"},
                    "lotSizeFilter": {"qtyStep": "0.001", "minOrderQty": "0.001"},
                }
            ]
        }
    }

    async def fake_get_json(_: str):
        return payload

    adapter._get_json = fake_get_json  # type: ignore[method-assign]
    instruments = asyncio.run(adapter.fetch_instruments())

    assert len(instruments) == 1
    assert instruments[0].canonical_symbol == "BTC/USDT:USDT"
