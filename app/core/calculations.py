from decimal import Decimal


def spread_pct(buy_ask: Decimal, sell_bid: Decimal) -> Decimal:
    if buy_ask <= 0:
        return Decimal("0")
    return (sell_bid / buy_ask - Decimal("1")) * Decimal("100")


def fee_pct(taker_buy_bps: Decimal, taker_sell_bps: Decimal) -> Decimal:
    return (taker_buy_bps + taker_sell_bps) / Decimal("100")


def slippage_pct(default_bps: Decimal, depth_penalty_bps: Decimal = Decimal("0")) -> Decimal:
    return (default_bps + depth_penalty_bps) / Decimal("100")


def net_spread_pct(
    gross_spread: Decimal,
    fee_estimate: Decimal,
    slippage_estimate: Decimal,
    execution_buffer_pct: Decimal,
) -> Decimal:
    return gross_spread - fee_estimate - slippage_estimate - execution_buffer_pct


def funding_net_pct(
    funding_receive_pct: Decimal,
    funding_pay_pct: Decimal,
    fee_estimate_pct: Decimal,
    slippage_estimate_pct: Decimal,
    basis_risk_buffer_pct: Decimal,
) -> Decimal:
    return (
        funding_receive_pct
        - funding_pay_pct
        - fee_estimate_pct
        - slippage_estimate_pct
        - basis_risk_buffer_pct
    )
