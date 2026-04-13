from app.exchange_adapters.bingx.adapter import BingXAdapter
from app.exchange_adapters.bybit.adapter import BybitAdapter
from app.exchange_adapters.gate.adapter import GateAdapter
from app.exchange_adapters.kucoin.adapter import KuCoinAdapter
from app.exchange_adapters.okx.adapter import OKXAdapter


def build_adapters():
    return [BybitAdapter(), OKXAdapter(), KuCoinAdapter(), BingXAdapter(), GateAdapter()]
