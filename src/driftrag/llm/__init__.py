"""LLM access (ADR-0004): one small interface, composed of single-purpose wrappers.

    CachedLLMClient     identical request already answered -> return it (free, reproducible)
      FallbackClient    on rate limits, outages or an exhausted budget, try the next model
        BudgetGuard     refuse when today's cap for *that model's* provider is reached
          LiteLLMClient the real provider call (Gemini, Groq, ...)

``build_llm_client`` assembles the chain from settings. Tests use ``FakeLLMClient``.
"""

from driftrag.llm.client import (
    Completion,
    CompletionRequest,
    LLMClient,
    LLMError,
    Message,
    RetryableLLMError,
)

__all__ = [
    "Completion",
    "CompletionRequest",
    "LLMClient",
    "LLMError",
    "Message",
    "RetryableLLMError",
]
