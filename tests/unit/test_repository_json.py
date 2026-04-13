from decimal import Decimal

from app.core.json_utils import to_json_safe
from app.core.types import ContractType


def test_json_safe_converts_decimal_and_enum():
    payload = {
        "x": Decimal("1.23"),
        "t": ContractType.LINEAR,
        "nested": {"y": Decimal("2.34")},
    }
    converted = to_json_safe(payload)
    assert converted == {"x": "1.23", "t": "linear", "nested": {"y": "2.34"}}
