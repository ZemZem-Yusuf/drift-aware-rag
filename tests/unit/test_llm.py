from pathlib import Path
from types import SimpleNamespace
from typing import Any

import litellm
import pytest
from litellm.exceptions import RateLimitError
from pydantic import SecretStr

from driftrag.config import Settings
from driftrag.llm.cache import BudgetGuard, CachedLLMClient
from driftrag.llm.client import (
    BudgetExceededError,
    CompletionRequest,
    FakeLLMClient,
    FallbackClient,
    LiteLLMClient,
    LLMError,
    Message,
    RetryableLLMError,
)
from driftrag.llm.factory import build_llm_client


def request(
    model: str = "gemini/flash", text: str = "hello", temperature: float = 0.0
) -> CompletionRequest:
    return CompletionRequest(
        model=model,
        messages=(Message("system", "be brief"), Message("user", text)),
        temperature=temperature,
    )


# ---------------------------------------------------------------- request
def test_provider_and_cache_key() -> None:
    assert request("groq/llama").provider == "groq"
    assert request().cache_key() == request().cache_key()
    assert request().cache_key() != request(text="hello!").cache_key()
    assert request().cache_key() != request(temperature=0.7).cache_key()
    assert request().cache_key() != request(model="gemini/pro").cache_key()


def test_fake_client_echoes_and_records() -> None:
    fake = FakeLLMClient()
    assert fake.complete(request(text="ping")).text == "ping"
    assert len(fake.requests) == 1


# ---------------------------------------------------------------- fallback
def test_fallback_on_retryable_error() -> None:
    fake = FakeLLMClient(errors=[RetryableLLMError("rate limited")])
    client = FallbackClient(fake, {"gemini/flash": ["groq/llama"]})
    completion = client.complete(request())
    assert completion.model == "groq/llama"
    assert [r.model for r in fake.requests] == ["gemini/flash", "groq/llama"]


def test_no_fallback_on_non_retryable_error() -> None:
    fake = FakeLLMClient(errors=[LLMError("bad request")])
    with pytest.raises(LLMError, match="bad request"):
        FallbackClient(fake, {"gemini/flash": ["groq/llama"]}).complete(request())
    assert len(fake.requests) == 1


def test_all_models_failing_raises_the_last_error() -> None:
    fake = FakeLLMClient(errors=[RetryableLLMError("first"), RetryableLLMError("second")])
    with pytest.raises(RetryableLLMError, match="second"):
        FallbackClient(fake, {"gemini/flash": ["groq/llama"]}).complete(request())


# ---------------------------------------------------------------- cache
def test_cache_returns_stored_answer_without_calling_the_provider(tmp_path: Path) -> None:
    fake = FakeLLMClient()
    client = CachedLLMClient(fake, tmp_path / "llm.sqlite")

    first = client.complete(request())
    second = client.complete(request())

    assert (first.cached, second.cached) == (False, True)
    assert second.text == first.text
    assert len(fake.requests) == 1


def test_cache_survives_restarts_and_misses_on_any_change(tmp_path: Path) -> None:
    path = tmp_path / "llm.sqlite"
    CachedLLMClient(FakeLLMClient(), path).complete(request())

    fake = FakeLLMClient()
    restarted = CachedLLMClient(fake, path)
    assert restarted.complete(request()).cached
    assert not restarted.complete(request(temperature=0.5)).cached
    assert len(fake.requests) == 1


def test_failed_calls_are_not_cached(tmp_path: Path) -> None:
    fake = FakeLLMClient(errors=[RetryableLLMError("down")])
    client = CachedLLMClient(fake, tmp_path / "llm.sqlite")
    with pytest.raises(RetryableLLMError):
        client.complete(request())
    assert not client.complete(request()).cached


# ---------------------------------------------------------------- budget
def test_budget_blocks_after_the_daily_limit(tmp_path: Path) -> None:
    guard = BudgetGuard(FakeLLMClient(), tmp_path / "llm.sqlite", {"gemini": 2})
    guard.complete(request(text="1"))
    guard.complete(request(text="2"))
    with pytest.raises(BudgetExceededError, match="2/2"):
        guard.complete(request(text="3"))
    assert guard.used_today("gemini") == 2
    guard.complete(request(model="groq/llama"))  # other providers are counted separately


def test_failed_calls_still_use_budget(tmp_path: Path) -> None:
    guard = BudgetGuard(
        FakeLLMClient(errors=[RetryableLLMError("down")]), tmp_path / "llm.sqlite", {"gemini": 5}
    )
    with pytest.raises(RetryableLLMError):
        guard.complete(request())
    assert guard.used_today("gemini") == 1


def test_exhausted_budget_falls_back_to_another_provider(tmp_path: Path) -> None:
    fake = FakeLLMClient()
    guard = BudgetGuard(fake, tmp_path / "llm.sqlite", {"gemini": 0})
    completion = FallbackClient(guard, {"gemini/flash": ["groq/llama"]}).complete(request())
    assert completion.model == "groq/llama"
    assert [r.model for r in fake.requests] == ["groq/llama"]


# ---------------------------------------------------------------- LiteLLM client
def fake_response(text: str) -> Any:
    return SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=text))],
        usage=SimpleNamespace(prompt_tokens=12, completion_tokens=3),
        model="gemini-2.5-flash",
    )


def test_litellm_client_passes_the_key_explicitly(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: dict[str, Any] = {}

    def completion(**kwargs: Any) -> Any:
        seen.update(kwargs)
        return fake_response("OK")

    monkeypatch.setattr(litellm, "completion", completion)
    monkeypatch.setattr(litellm, "completion_cost", lambda **_: 0.0001)
    client = LiteLLMClient({"gemini": SecretStr("test-key")})

    result = client.complete(request())

    assert seen["api_key"] == "test-key"
    assert seen["messages"][1] == {"role": "user", "content": "hello"}
    assert (result.text, result.input_tokens, result.output_tokens) == ("OK", 12, 3)
    assert result.cost_usd == pytest.approx(0.0001)


def test_litellm_client_unknown_cost_is_none(monkeypatch: pytest.MonkeyPatch) -> None:
    def no_price(**_: Any) -> float:
        raise ValueError("model not in price map")

    monkeypatch.setattr(litellm, "completion", lambda **_: fake_response("OK"))
    monkeypatch.setattr(litellm, "completion_cost", no_price)
    assert LiteLLMClient({"gemini": SecretStr("k")}).complete(request()).cost_usd is None


def test_litellm_rate_limit_is_retryable(monkeypatch: pytest.MonkeyPatch) -> None:
    def rate_limited(**_: Any) -> Any:
        raise RateLimitError(message="429", llm_provider="gemini", model="flash")

    monkeypatch.setattr(litellm, "completion", rate_limited)
    with pytest.raises(RetryableLLMError, match="RateLimitError"):
        LiteLLMClient({"gemini": SecretStr("k")}).complete(request())


def test_missing_key_is_a_clear_error() -> None:
    with pytest.raises(LLMError, match="no API key"):
        LiteLLMClient({}).complete(request())


# ---------------------------------------------------------------- settings and factory
def test_provider_keys_come_from_their_usual_env_names(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GEMINI_API_KEY", "from-env-123")
    settings = Settings(_env_file=None)
    assert settings.gemini_api_key is not None
    assert settings.gemini_api_key.get_secret_value() == "from-env-123"
    assert "from-env-123" not in repr(settings)


def test_factory_builds_the_chain(tmp_path: Path) -> None:
    settings = Settings(_env_file=None, llm_cache_path=tmp_path / "llm.sqlite")
    client = build_llm_client(settings)
    assert isinstance(client, CachedLLMClient)
