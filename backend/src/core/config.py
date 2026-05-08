"""Application settings loaded from environment and optional `.env` file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Twelve-factor settings loaded from the process environment (and optional ``.env``).

    This type is the only supported configuration entrypoint for the backend.
    ``DATABASE_URL`` must be supplied for any process that opens a DB session
    (including API startup, which verifies connectivity in ``lifespan``).
    """

    VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
