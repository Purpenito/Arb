def to_sync_dsn(dsn: str) -> str:
    """Convert async SQLAlchemy postgres DSN to sync driver DSN for Alembic."""
    if dsn.startswith("postgresql+asyncpg://"):
        return dsn.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    return dsn
