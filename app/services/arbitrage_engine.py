from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.calculations import fee_pct, funding_net_pct, net_spread_pct, slippage_pct, spread_pct
from app.core.freshness import is_stale
from app.core.symbols import compatible_for_arb
from app.core.types import ContractType, InstrumentType
from app.infra.config import get_settings
from app.storage.models import (
    BestQuote,
    Exchange,
    FundingCurrent,
    FundingOpportunity,
    FuturesFuturesOpportunity,
    Instrument,
)


@dataclass
class OpportunityResult:
    futures: list[dict]
    funding: list[dict]


class ArbitrageEngine:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.settings = get_settings()

    async def compute(self) -> OpportunityResult:
        futures = await self._compute_futures_futures()
        funding = await self._compute_funding()
        return OpportunityResult(futures=futures, funding=funding)

    async def _latest_quotes(self) -> list[tuple[BestQuote, Instrument, Exchange]]:
        rows = await self.session.execute(
            select(BestQuote, Instrument, Exchange)
            .join(Instrument, Instrument.id == BestQuote.instrument_id)
            .join(Exchange, Exchange.id == Instrument.exchange_id)
            .order_by(BestQuote.ts.desc())
        )
        latest_by_inst: dict[int, tuple[BestQuote, Instrument, Exchange]] = {}
        for bq, inst, ex in rows.all():
            if inst.id not in latest_by_inst:
                latest_by_inst[inst.id] = (bq, inst, ex)
        return list(latest_by_inst.values())

    async def _compute_futures_futures(self) -> list[dict]:
        now = datetime.now(timezone.utc)
        grouped: dict[str, list[tuple[BestQuote, Instrument, Exchange]]] = defaultdict(list)
        for bq, inst, ex in await self._latest_quotes():
            if is_stale(bq.ts, self.settings.quote_stale_ms):
                continue
            grouped[inst.canonical_symbol].append((bq, inst, ex))

        results: list[dict] = []
        for symbol, rows in grouped.items():
            for buy_q, buy_inst, buy_ex in rows:
                for sell_q, sell_inst, sell_ex in rows:
                    if buy_ex.id == sell_ex.id:
                        continue
                    if not compatible_for_arb(
                        ContractType(buy_inst.contract_type),
                        ContractType(sell_inst.contract_type),
                        InstrumentType(buy_inst.instrument_type),
                        InstrumentType(sell_inst.instrument_type),
                        buy_inst.canonical_symbol,
                        sell_inst.canonical_symbol,
                    ):
                        continue
                    gross = spread_pct(buy_q.ask, sell_q.bid)
                    fee = fee_pct(Decimal(buy_ex.taker_fee_bps), Decimal(sell_ex.taker_fee_bps))
                    slip = slippage_pct(Decimal(str(self.settings.default_slippage_bps)))
                    net = net_spread_pct(gross, fee, slip, Decimal(str(self.settings.execution_buffer_pct)))
                    max_notional = min(buy_q.ask_size * buy_q.ask, sell_q.bid_size * sell_q.bid)
                    freshness = int(max((now - buy_q.ts).total_seconds(), (now - sell_q.ts).total_seconds()) * 1000)
                    confidence = Decimal("1") if net > 0 else Decimal("0.25")
                    self.session.add(
                        FuturesFuturesOpportunity(
                            canonical_symbol=symbol,
                            buy_exchange_id=buy_ex.id,
                            sell_exchange_id=sell_ex.id,
                            buy_ask=buy_q.ask,
                            sell_bid=sell_q.bid,
                            gross_spread_pct=gross,
                            fee_estimate_pct=fee,
                            slippage_estimate_pct=slip,
                            net_spread_pct=net,
                            max_tradable_notional=max_notional,
                            freshness_ms=freshness,
                            confidence_score=confidence,
                            ts=now,
                        )
                    )
                    results.append(
                        {
                            "canonical_symbol": symbol,
                            "buy_exchange": buy_ex.name,
                            "sell_exchange": sell_ex.name,
                            "buy_ask": buy_q.ask,
                            "sell_bid": sell_q.bid,
                            "gross_spread_pct": gross,
                            "net_spread_pct": net,
                            "fee_estimate_pct": fee,
                            "slippage_estimate_pct": slip,
                            "max_tradable_notional": max_notional,
                            "freshness_ms": freshness,
                            "confidence_score": confidence,
                            "ts": now,
                        }
                    )
        return sorted(results, key=lambda x: x["net_spread_pct"], reverse=True)

    async def _compute_funding(self) -> list[dict]:
        now = datetime.now(timezone.utc)
        q = await self.session.execute(
            select(FundingCurrent, Instrument, Exchange)
            .join(Instrument, Instrument.id == FundingCurrent.instrument_id)
            .join(Exchange, Exchange.id == Instrument.exchange_id)
        )
        grouped: dict[str, list[tuple[FundingCurrent, Instrument, Exchange]]] = defaultdict(list)
        for fc, inst, ex in q.all():
            grouped[inst.canonical_symbol].append((fc, inst, ex))

        results = []
        for symbol, rows in grouped.items():
            for r_fc, r_inst, r_ex in rows:
                for h_fc, h_inst, h_ex in rows:
                    if r_ex.id == h_ex.id:
                        continue
                    if not compatible_for_arb(
                        ContractType(r_inst.contract_type),
                        ContractType(h_inst.contract_type),
                        InstrumentType(r_inst.instrument_type),
                        InstrumentType(h_inst.instrument_type),
                        r_inst.canonical_symbol,
                        h_inst.canonical_symbol,
                    ):
                        continue
                    recv = Decimal(r_fc.funding_rate) * Decimal("100")
                    pay = Decimal(h_fc.funding_rate) * Decimal("100")
                    fee = fee_pct(Decimal(r_ex.taker_fee_bps), Decimal(h_ex.taker_fee_bps))
                    slip = slippage_pct(Decimal(str(self.settings.default_slippage_bps)))
                    net = funding_net_pct(recv, pay, fee, slip, Decimal(str(self.settings.basis_risk_buffer_pct)))
                    primary_side = "short" if recv >= 0 else "long"
                    hedge_side = "long" if primary_side == "short" else "short"
                    self.session.add(
                        FundingOpportunity(
                            canonical_symbol=symbol,
                            receive_exchange_id=r_ex.id,
                            hedge_exchange_id=h_ex.id,
                            primary_leg_side=primary_side,
                            hedge_leg_side=hedge_side,
                            funding_receive_pct=recv,
                            funding_pay_pct=pay,
                            fee_estimate_pct=fee,
                            slippage_estimate_pct=slip,
                            net_expected_pct=net,
                            next_funding_time=r_fc.next_funding_time,
                            max_tradable_notional=Decimal("10000"),
                            confidence_score=Decimal("1") if net > 0 else Decimal("0.2"),
                            ts=now,
                        )
                    )
                    results.append(
                        {
                            "canonical_symbol": symbol,
                            "receive_exchange": r_ex.name,
                            "hedge_exchange": h_ex.name,
                            "primary_leg_side": primary_side,
                            "hedge_leg_side": hedge_side,
                            "funding_receive_pct": recv,
                            "funding_pay_pct": pay,
                            "fee_estimate_pct": fee,
                            "slippage_estimate_pct": slip,
                            "net_expected_pct": net,
                            "next_funding_time": r_fc.next_funding_time,
                            "max_tradable_notional": Decimal("10000"),
                            "confidence_score": Decimal("1") if net > 0 else Decimal("0.2"),
                            "ts": now,
                        }
                    )
        return sorted(results, key=lambda x: x["net_expected_pct"], reverse=True)
