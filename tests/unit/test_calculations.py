from decimal import Decimal
from app.core.calculations import funding_net_pct, net_spread_pct, spread_pct


def test_futures_spread_calc():
    gross = spread_pct(Decimal("100"), Decimal("101"))
    assert gross == Decimal("1.00")
    net = net_spread_pct(gross, Decimal("0.10"), Decimal("0.05"), Decimal("0.02"))
    assert net == Decimal("0.83")


def test_funding_calc():
    net = funding_net_pct(
        funding_receive_pct=Decimal("0.020"),
        funding_pay_pct=Decimal("0.005"),
        fee_estimate_pct=Decimal("0.010"),
        slippage_estimate_pct=Decimal("0.002"),
        basis_risk_buffer_pct=Decimal("0.001"),
    )
    assert net == Decimal("0.002")
