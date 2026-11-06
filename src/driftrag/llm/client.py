"""Core LLM types, the provider client (LiteLLM), a fallback wrapper and a fake for tests."""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from typing import Literal, Protocol

from pydantic import SecretStr

Role = Literal["system", "user", "assistant"]


class LLMError(RuntimeError):
    """A model call failed and retrying the same model won't help (bad request, auth, ...)."""


class RetryableLLMError(LLMError):
    """Rate limit, timeout or provider outage: another attempt or another model may succeed."""


class BudgetExceededError(RetryableLLMError):
    """The daily request cap for a provider is reached (another provider may still have budget)."""


@dataclass(frozen=True)
class Message:
    role: Role
    content: str


@dataclass(frozen=True)
class CompletionRequest:
    model: str
    messages: tuple[Message, ...]
    temperature: float = 0.0
    max_tokens: int = 1024

    @property
    def provider(self) -> str:
        """``gemini/gemini-2.5-flash`` -> ``gemini``."""
        return self.model.split("/", 1)[0]

    def with_model(self, model: str) -> CompletionRequest:
        return CompletionRequest(model, self.messages, self.temperature, self.max_tokens)

    def cache_key(self) -> str:
        """Stable hash of everything that affects the answer."""
        payload = json.dumps(asdict(self), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Completion:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float | None
    latency_ms: float
    cached: bool = False


class LLMClient(Protocol):
    def complete(self, request: CompletionRequest) -> Completion: ...


class LiteLLMClient:
    """Calls providers through the LiteLLM SDK (one API over Gemini, Groq, OpenAI, Bedrock...).

    API keys are passed explicitly per call, never through global environment variables, so a
    key only ever goes to its own provider.
    """

    def __init__(
        self,
        api_keys: Mapping[str, SecretStr],
        *,
        timeout_s: float = 60.0,
        num_retries: int = 2,
    ) -> None:
        self._api_keys = dict(api_keys)
        self._timeout_s = timeout_s
        self._num_retries = num_retries

    def complete(self, request: CompletionRequest) -> Completion:
        # Imported lazily: litellm is slow to import and unused in most code paths.
        import litellm
        from litellm.exceptions import (
            APIConnectionError,
            InternalServerError,
            RateLimitError,
            ServiceUnavailableError,
            Timeout,
        )

        key = self._api_keys.get(request.provider)
        if key is None:
            raise LLMError(f"no API key configured for provider '{request.provider}'")
        started = time.perf_counter()
        try:
            response = litellm.completion(
                model=request.model,
                messages=[{"role": m.role, "content": m.content} for m in request.messages],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                api_key=key.get_secret_value(),
                timeout=self._timeout_s,
                num_retries=self._num_retries,
            )
        except (
            RateLimitError,
            Timeout,
            APIConnectionError,
            ServiceUnavailableError,
            InternalServerError,
        ) as exc:
            raise RetryableLLMError(f"{request.model}: {type(exc).__name__}") from exc
        except Exception as exc:
            # Message only: provider errors can echo request details, never the key itself
            # (it isn't part of the message), but keep logs short anyway.
            raise LLMError(f"{request.model}: {type(exc).__name__}: {exc}"[:500]) from exc
        latency_ms = (time.perf_counter() - started) * 1000
        usage = getattr(response, "usage", None)
        try:
            cost: float | None = float(litellm.completion_cost(completion_response=response))
        except Exception:
            cost = None  # unknown price (e.g. new or free model): record as unknown, not 0
        return Completion(
            text=response.choices[0].message.content or "",
            model=str(getattr(response, "model", request.model) or request.model),
            input_tokens=int(getattr(usage, "prompt_tokens", 0) or 0),
            output_tokens=int(getattr(usage, "completion_tokens", 0) or 0),
            cost_usd=cost,
            latency_ms=latency_ms,
        )


class FallbackClient:
    """On a retryable error, try the fallback models in order. Other errors are raised as is."""

    def __init__(self, inner: LLMClient, fallbacks: Mapping[str, Sequence[str]]) -> None:
        self._inner = inner
        self._fallbacks = {model: list(chain) for model, chain in fallbacks.items()}

    def complete(self, request: CompletionRequest) -> Completion:
        models = [request.model, *self._fallbacks.get(request.model, [])]
        last_error: RetryableLLMError | None = None
        for model in models:
            try:
                return self._inner.complete(request.with_model(model))
            except RetryableLLMError as exc:
                last_error = exc
        if last_error is None:  # pragma: no cover - the list always contains request.model
            raise LLMError("no model to try")
        raise last_error


@dataclass
class FakeLLMClient:
    """Deterministic stand-in for tests and CI. Records every request it receives.

    ``responder`` builds the answer from the request; by default it echoes the last user
    message. ``errors`` are raised (in order) before any answer is returned.
    """

    responder: Callable[[CompletionRequest], str] | None = None
    errors: list[LLMError] = field(default_factory=list)
    requests: list[CompletionRequest] = field(default_factory=list)

    def complete(self, request: CompletionRequest) -> Completion:
        self.requests.append(request)
        if self.errors:
            raise self.errors.pop(0)
        if self.responder is not None:
            text = self.responder(request)
        else:
            text = next(m.content for m in reversed(request.messages) if m.role == "user")
        return Completion(
            text=text,
            model=request.model,
            input_tokens=sum(len(m.content.split()) for m in request.messages),
            output_tokens=len(text.split()),
            cost_usd=0.0,
            latency_ms=0.0,
        )
