from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "arb-scanner"
    env: str = "dev"
    log_level: str = "INFO"

    postgres_dsn: str = Field(default="postgresql+asyncpg://arb:arb@db:5432/arb")
    redis_url: str = Field(default="redis://redis:6379/0")

    quote_stale_ms: int = 3000
    execution_buffer_pct: float = 0.03
    basis_risk_buffer_pct: float = 0.02
    default_slippage_bps: float = 2.0

    collector_interval_seconds: int = 5


@lru_cache
def get_settings() -> Settings:
    return Settings()
