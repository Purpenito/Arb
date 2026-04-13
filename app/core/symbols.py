from app.core.types import ContractType, InstrumentType


def canonical_symbol(base: str, quote: str, settle: str) -> str:
    return f"{base.upper()}/{quote.upper()}:{settle.upper()}"


def compatible_for_arb(
    left_contract: ContractType,
    right_contract: ContractType,
    left_instr: InstrumentType,
    right_instr: InstrumentType,
    left_symbol: str,
    right_symbol: str,
) -> bool:
    return (
        left_contract == right_contract
        and left_instr == right_instr
        and left_symbol == right_symbol
    )
