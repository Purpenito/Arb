def to_sync_dsn(dsn: str) -> str:
    """Normalize DB DSNs for Alembic sync engine usage.

    Rules:
    - postgresql+asyncpg:// -> postgresql+psycopg://
    - postgresql:// -> postgresql+psycopg:// (avoid psycopg2 fallback)
    - postgres:// -> postgresql+psycopg://
    """
    if dsn.startswith("postgresql+asyncpg://"):
        return dsn.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
    if dsn.startswith("postgresql://"):
        return dsn.replace("postgresql://", "postgresql+psycopg://", 1)
    if dsn.startswith("postgres://"):
        return dsn.replace("postgres://", "postgresql+psycopg://", 1)
    return dsn
