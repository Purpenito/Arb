from enum import StrEnum


class ArbitrageType(StrEnum):
    SPOT_FUTURES = 'spot_futures'
    FUTURES_FUTURES = 'futures_futures'
    FUNDING = 'funding'


class MarketType(StrEnum):
    SPOT = 'spot'
    FUTURES = 'futures'
