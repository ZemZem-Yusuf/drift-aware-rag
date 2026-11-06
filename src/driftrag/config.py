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
    # 127.0.0.1 rather than localhost: on Windows, localhost tries IPv6 first and Docker only
    # publishes the port on IPv4, which adds a ~10 s delay to every new connection.
    database_url: SecretStr = Field(
        default=SecretStr("postgresql://driftrag:driftrag@127.0.0.1:5433/driftrag"),
        description="Postgres DSN. Secret so it never appears in logs or reprs.",
    )

    # LLM access (ADR-0004). Model ids use LiteLLM's "<provider>/<model>" form.
    generator_model: str = "gemini/gemini-2.5-flash"
    fallback_model: str | None = Field(
        default=None, description="Tried when the generator is rate-limited or over budget."
    )
    llm_cache_path: Path = Path("data/cache/llm.sqlite")
    llm_daily_request_limits: dict[str, int] = Field(
        default_factory=lambda: {"gemini": 200, "groq": 500},
        description="Real provider calls per UTC day; kept under the free-tier caps.",
    )
    # Provider keys use their usual names (no DRIFTRAG_ prefix) and are never logged.
    gemini_api_key: SecretStr | None = Field(default=None, validation_alias="GEMINI_API_KEY")
    groq_api_key: SecretStr | None = Field(default=None, validation_alias="GROQ_API_KEY")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide settings (cached). Tests can call ``get_settings.cache_clear()``."""
    return Settings()
