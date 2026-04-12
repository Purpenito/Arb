from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_prefix='ARB_')

    app_name: str = 'Arb Monitor API'
    env: str = 'dev'
    postgres_dsn: str = 'postgresql+asyncpg://postgres:postgres@localhost:5432/arb'
    redis_url: str = 'redis://localhost:6379/0'
    websocket_tick_ms: int = 2000


settings = Settings()
