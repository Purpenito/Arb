import asyncio

from app.exchange_adapters.kucoin.adapter import KuCoinAdapter


def test_kucoin_ticker_shape_list_supported():
    adapter = KuCoinAdapter()
    payload = {
        "data": [
            {
                "symbol": "BTCUSDTM",
                "bestBidPrice": "100",
                "bestAskPrice": "101",
                "bestBidSize": "10",
                "bestAskSize": "11",
                "fundingFeeRate": "0.0001",
            }
        ]
    }

    async def fake_get_json(_: str):
        return payload

    adapter._get_json = fake_get_json  # type: ignore[method-assign]
    tobs = asyncio.run(adapter.fetch_top_of_book_snapshot())
    fund = asyncio.run(adapter.fetch_current_funding())

    assert len(tobs) == 1
    assert len(fund) == 1
    assert tobs[0].canonical_symbol == "BTC/USDT:USDT"
