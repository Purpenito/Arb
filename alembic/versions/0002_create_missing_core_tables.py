"""create missing core tables

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-13
"""

from alembic import op
import sqlalchemy as sa


revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def _has_table(bind, table_name: str) -> bool:
    insp = sa.inspect(bind)
    return table_name in insp.get_table_names()


def upgrade() -> None:
    bind = op.get_bind()

    if not _has_table(bind, "instruments"):
        op.create_table(
            "instruments",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("exchange_id", sa.Integer(), sa.ForeignKey("exchanges.id"), nullable=False),
            sa.Column("native_symbol", sa.String(100), nullable=False),
            sa.Column("canonical_symbol", sa.String(100), nullable=False),
            sa.Column("base_asset", sa.String(20), nullable=False),
            sa.Column("quote_asset", sa.String(20), nullable=False),
            sa.Column("settle_asset", sa.String(20), nullable=False),
            sa.Column("contract_type", sa.String(20), nullable=False),
            sa.Column("instrument_type", sa.String(20), nullable=False),
            sa.Column("tick_size", sa.Numeric(30, 12), nullable=False),
            sa.Column("qty_step", sa.Numeric(30, 12), nullable=False),
            sa.Column("min_qty", sa.Numeric(30, 12), nullable=False),
            sa.Column("contract_size", sa.Numeric(30, 12), nullable=False),
            sa.Column("funding_interval_minutes", sa.Integer(), nullable=True),
            sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
            sa.Column("raw_metadata_json", sa.JSON(), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index("ix_instruments_exchange_id", "instruments", ["exchange_id"])
        op.create_index("ix_instruments_native_symbol", "instruments", ["native_symbol"])
        op.create_index("ix_instruments_canonical_symbol", "instruments", ["canonical_symbol"])

    if not _has_table(bind, "best_quotes"):
        op.create_table(
            "best_quotes",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id"), nullable=False),
            sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
            sa.Column("bid", sa.Numeric(30, 12), nullable=False),
            sa.Column("ask", sa.Numeric(30, 12), nullable=False),
            sa.Column("bid_size", sa.Numeric(30, 12), nullable=False),
            sa.Column("ask_size", sa.Numeric(30, 12), nullable=False),
            sa.Column("mark_price", sa.Numeric(30, 12), nullable=True),
            sa.Column("index_price", sa.Numeric(30, 12), nullable=True),
            sa.Column("last_price_optional", sa.Numeric(30, 12), nullable=True),
            sa.Column("is_stale", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        )
        op.create_index("ix_best_quotes_instrument_id", "best_quotes", ["instrument_id"])
        op.create_index("ix_best_quotes_ts", "best_quotes", ["ts"])

    if not _has_table(bind, "funding_current"):
        op.create_table(
            "funding_current",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id"), nullable=False),
            sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
            sa.Column("funding_rate", sa.Numeric(20, 12), nullable=False),
            sa.Column("next_funding_time", sa.DateTime(timezone=True), nullable=True),
            sa.Column("funding_interval_minutes", sa.Integer(), nullable=True),
            sa.Column("mark_price", sa.Numeric(30, 12), nullable=True),
            sa.Column("predicted_flag", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        )
        op.create_index("ix_funding_current_instrument_id", "funding_current", ["instrument_id"])
        op.create_index("ix_funding_current_ts", "funding_current", ["ts"])

    if not _has_table(bind, "funding_history"):
        op.create_table(
            "funding_history",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("instrument_id", sa.Integer(), sa.ForeignKey("instruments.id"), nullable=False),
            sa.Column("funding_time", sa.DateTime(timezone=True), nullable=False),
            sa.Column("funding_rate", sa.Numeric(20, 12), nullable=False),
            sa.Column("mark_price_optional", sa.Numeric(30, 12), nullable=True),
        )
        op.create_index("ix_funding_history_instrument_id", "funding_history", ["instrument_id"])
        op.create_index("ix_funding_history_funding_time", "funding_history", ["funding_time"])

    if not _has_table(bind, "futures_futures_opportunities"):
        op.create_table(
            "futures_futures_opportunities",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("canonical_symbol", sa.String(100), nullable=False),
            sa.Column("buy_exchange_id", sa.Integer(), sa.ForeignKey("exchanges.id"), nullable=False),
            sa.Column("sell_exchange_id", sa.Integer(), sa.ForeignKey("exchanges.id"), nullable=False),
            sa.Column("buy_ask", sa.Numeric(30, 12), nullable=False),
            sa.Column("sell_bid", sa.Numeric(30, 12), nullable=False),
            sa.Column("gross_spread_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("fee_estimate_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("slippage_estimate_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("net_spread_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("max_tradable_notional", sa.Numeric(30, 12), nullable=False),
            sa.Column("freshness_ms", sa.Integer(), nullable=False),
            sa.Column("confidence_score", sa.Numeric(10, 6), nullable=False),
            sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index("ix_ffo_canonical_symbol", "futures_futures_opportunities", ["canonical_symbol"])
        op.create_index("ix_ffo_buy_exchange_id", "futures_futures_opportunities", ["buy_exchange_id"])
        op.create_index("ix_ffo_sell_exchange_id", "futures_futures_opportunities", ["sell_exchange_id"])
        op.create_index("ix_ffo_ts", "futures_futures_opportunities", ["ts"])

    if not _has_table(bind, "funding_opportunities"):
        op.create_table(
            "funding_opportunities",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("canonical_symbol", sa.String(100), nullable=False),
            sa.Column("receive_exchange_id", sa.Integer(), sa.ForeignKey("exchanges.id"), nullable=False),
            sa.Column("hedge_exchange_id", sa.Integer(), sa.ForeignKey("exchanges.id"), nullable=False),
            sa.Column("primary_leg_side", sa.String(10), nullable=False),
            sa.Column("hedge_leg_side", sa.String(10), nullable=False),
            sa.Column("funding_receive_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("funding_pay_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("fee_estimate_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("slippage_estimate_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("net_expected_pct", sa.Numeric(20, 8), nullable=False),
            sa.Column("next_funding_time", sa.DateTime(timezone=True), nullable=True),
            sa.Column("max_tradable_notional", sa.Numeric(30, 12), nullable=False),
            sa.Column("confidence_score", sa.Numeric(10, 6), nullable=False),
            sa.Column("ts", sa.DateTime(timezone=True), nullable=False),
        )
        op.create_index("ix_fo_canonical_symbol", "funding_opportunities", ["canonical_symbol"])
        op.create_index("ix_fo_receive_exchange_id", "funding_opportunities", ["receive_exchange_id"])
        op.create_index("ix_fo_hedge_exchange_id", "funding_opportunities", ["hedge_exchange_id"])
        op.create_index("ix_fo_ts", "funding_opportunities", ["ts"])

    if not _has_table(bind, "connector_state"):
        op.create_table(
            "connector_state",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("exchange_id", sa.Integer(), sa.ForeignKey("exchanges.id"), nullable=False, unique=True),
            sa.Column("status", sa.String(20), nullable=False, server_default="ok"),
            sa.Column("last_heartbeat", sa.DateTime(timezone=True), nullable=False),
            sa.Column("last_error", sa.String(500), nullable=True),
        )
        op.create_index("ix_connector_state_last_heartbeat", "connector_state", ["last_heartbeat"])


def downgrade() -> None:
    bind = op.get_bind()

    if _has_table(bind, "connector_state"):
        op.drop_index("ix_connector_state_last_heartbeat", table_name="connector_state")
        op.drop_table("connector_state")

    if _has_table(bind, "funding_opportunities"):
        op.drop_index("ix_fo_ts", table_name="funding_opportunities")
        op.drop_index("ix_fo_hedge_exchange_id", table_name="funding_opportunities")
        op.drop_index("ix_fo_receive_exchange_id", table_name="funding_opportunities")
        op.drop_index("ix_fo_canonical_symbol", table_name="funding_opportunities")
        op.drop_table("funding_opportunities")

    if _has_table(bind, "futures_futures_opportunities"):
        op.drop_index("ix_ffo_ts", table_name="futures_futures_opportunities")
        op.drop_index("ix_ffo_sell_exchange_id", table_name="futures_futures_opportunities")
        op.drop_index("ix_ffo_buy_exchange_id", table_name="futures_futures_opportunities")
        op.drop_index("ix_ffo_canonical_symbol", table_name="futures_futures_opportunities")
        op.drop_table("futures_futures_opportunities")

    if _has_table(bind, "funding_history"):
        op.drop_index("ix_funding_history_funding_time", table_name="funding_history")
        op.drop_index("ix_funding_history_instrument_id", table_name="funding_history")
        op.drop_table("funding_history")

    if _has_table(bind, "funding_current"):
        op.drop_index("ix_funding_current_ts", table_name="funding_current")
        op.drop_index("ix_funding_current_instrument_id", table_name="funding_current")
        op.drop_table("funding_current")

    if _has_table(bind, "best_quotes"):
        op.drop_index("ix_best_quotes_ts", table_name="best_quotes")
        op.drop_index("ix_best_quotes_instrument_id", table_name="best_quotes")
        op.drop_table("best_quotes")

    if _has_table(bind, "instruments"):
        op.drop_index("ix_instruments_canonical_symbol", table_name="instruments")
        op.drop_index("ix_instruments_native_symbol", table_name="instruments")
        op.drop_index("ix_instruments_exchange_id", table_name="instruments")
        op.drop_table("instruments")
