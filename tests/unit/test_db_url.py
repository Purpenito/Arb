from app.storage.url import to_sync_dsn


def test_to_sync_dsn_from_asyncpg():
    assert to_sync_dsn("postgresql+asyncpg://u:p@db:5432/app") == "postgresql+psycopg://u:p@db:5432/app"


def test_to_sync_dsn_from_plain_postgresql():
    assert to_sync_dsn("postgresql://u:p@db:5432/app") == "postgresql+psycopg://u:p@db:5432/app"


def test_to_sync_dsn_from_postgres_alias():
    assert to_sync_dsn("postgres://u:p@db:5432/app") == "postgresql+psycopg://u:p@db:5432/app"


def test_to_sync_dsn_passthrough():
    dsn = "postgresql+psycopg://u:p@db:5432/app"
    assert to_sync_dsn(dsn) == dsn
