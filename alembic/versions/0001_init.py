"""init

Revision ID: 0001
Revises:
Create Date: 2026-04-13
"""

from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Keep migration compact for challenge; create all tables from metadata in real deployments.
    op.create_table('exchanges',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(32), nullable=False, unique=True),
        sa.Column('enabled', sa.Boolean(), nullable=False),
        sa.Column('taker_fee_bps', sa.Numeric(10,4), nullable=False),
        sa.Column('maker_fee_bps', sa.Numeric(10,4), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('exchanges')
