"""Application settings loaded from environment and optional `.env` file."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Twelve-factor settings loaded from the process environment (and optional ``.env``).

    This type is the only supported configuration entrypoint for the backend until
    database URLs and secrets are introduced in later epics.
    """

    VERSION: str = "0.1.0"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
