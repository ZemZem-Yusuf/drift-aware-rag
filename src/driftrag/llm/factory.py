"""Assemble the LLM client chain from settings."""

from __future__ import annotations

from pydantic import SecretStr

from driftrag.config import Settings
from driftrag.llm.cache import BudgetGuard, CachedLLMClient
from driftrag.llm.client import FallbackClient, LiteLLMClient, LLMClient


def build_llm_client(settings: Settings) -> LLMClient:
    api_keys: dict[str, SecretStr] = {}
    if settings.gemini_api_key is not None:
        api_keys["gemini"] = settings.gemini_api_key
    if settings.groq_api_key is not None:
        api_keys["groq"] = settings.groq_api_key

    provider_client = LiteLLMClient(api_keys)
    budgeted = BudgetGuard(
        provider_client, settings.llm_cache_path, settings.llm_daily_request_limits
    )
    fallbacks = (
        {settings.generator_model: [settings.fallback_model]} if settings.fallback_model else {}
    )
    return CachedLLMClient(FallbackClient(budgeted, fallbacks), settings.llm_cache_path)
