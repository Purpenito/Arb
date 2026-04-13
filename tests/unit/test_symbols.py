from app.core.symbols import canonical_symbol, compatible_for_arb
from app.core.types import ContractType, InstrumentType


def test_canonical_symbol():
    assert canonical_symbol("btc", "usdt", "usdt") == "BTC/USDT:USDT"


def test_compatibility_filter():
    assert compatible_for_arb(
        ContractType.LINEAR,
        ContractType.LINEAR,
        InstrumentType.PERPETUAL,
        InstrumentType.PERPETUAL,
        "BTC/USDT:USDT",
        "BTC/USDT:USDT",
    )
    assert not compatible_for_arb(
        ContractType.LINEAR,
        ContractType.INVERSE,
        InstrumentType.PERPETUAL,
        InstrumentType.PERPETUAL,
        "BTC/USDT:USDT",
        "BTC/USD:BTC",
    )
