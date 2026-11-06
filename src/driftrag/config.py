"""Application settings, loaded from environment variables (prefix ``DRIFTRAG_``) or ``.env``."""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Single source of configuration. No magic constants elsewhere in the code."""

    model_config = SettingsConfigDict(
        env_prefix="DRIFTRAG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    env: Literal["dev", "test", "prod"] = "dev"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    data_dir: Path = Path("data")
    database_url: SecretStr = Field(
        default=SecretStr("postgresql://driftrag:driftrag@localhost:5432/driftrag"),
        description="Postgres DSN. Secret so it never appears in logs or reprs.",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings (cached). Tests can call ``get_settings.cache_clear()``."""
    return Settings()
