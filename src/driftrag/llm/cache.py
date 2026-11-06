"""Response cache and daily request budget, both in one small SQLite file.

The cache makes experiments **reproducible and free to rerun**: an identical request (same model,
messages and parameters) returns the stored answer instead of calling the provider. The budget
keeps free-tier usage under the provider's daily cap, so a long experiment stops cleanly instead
of being cut off half-way by rate-limit errors.

Only real provider calls count against the budget; cache hits are free.
"""

from __future__ import annotations

import json
import sqlite3
import threading
from collections.abc import Mapping
from datetime import UTC, datetime
from pathlib import Path

from driftrag.llm.client import (
    BudgetExceededError,
    Completion,
    CompletionRequest,
    LLMClient,
)

_SCHEMA = """
CREATE TABLE IF NOT EXISTS responses (
    key            TEXT PRIMARY KEY,
    model          TEXT NOT NULL,
    request_json   TEXT NOT NULL,
    text           TEXT NOT NULL,
    served_model   TEXT NOT NULL,
    input_tokens   INTEGER NOT NULL,
    output_tokens  INTEGER NOT NULL,
    cost_usd       REAL,
    created_at     TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS usage (
    provider  TEXT NOT NULL,
    day       TEXT NOT NULL,
    requests  INTEGER NOT NULL,
    PRIMARY KEY (provider, day)
);
"""


class _Store:
    """One SQLite connection shared by threads (FastAPI runs sync handlers in a thread pool)."""

    def __init__(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        self.lock = threading.Lock()
        self.db = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.executescript(_SCHEMA)


_stores: dict[Path, _Store] = {}
_stores_lock = threading.Lock()


def _store(path: Path) -> _Store:
    resolved = path.resolve()
    with _stores_lock:
        if resolved not in _stores:
            _stores[resolved] = _Store(resolved)
        return _stores[resolved]


class CachedLLMClient:
    def __init__(self, inner: LLMClient, path: Path) -> None:
        self._inner = inner
        self._store = _store(path)

    def complete(self, request: CompletionRequest) -> Completion:
        key = request.cache_key()
        with self._store.lock:
            row = self._store.db.execute(
                "SELECT text, served_model, input_tokens, output_tokens, cost_usd "
                "FROM responses WHERE key = ?",
                (key,),
            ).fetchone()
        if row is not None:
            text, served_model, input_tokens, output_tokens, cost = row
            return Completion(
                text=text,
                model=served_model,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost,
                latency_ms=0.0,
                cached=True,
            )
        completion = self._inner.complete(request)
        with self._store.lock:
            self._store.db.execute(
                "INSERT OR REPLACE INTO responses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    key,
                    request.model,
                    json.dumps(
                        {
                            "messages": [m.__dict__ for m in request.messages],
                            "temperature": request.temperature,
                            "max_tokens": request.max_tokens,
                        },
                        ensure_ascii=False,
                    ),
                    completion.text,
                    completion.model,
                    completion.input_tokens,
                    completion.output_tokens,
                    completion.cost_usd,
                    datetime.now(UTC).isoformat(timespec="seconds"),
                ),
            )
        return completion


class BudgetGuard:
    """Caps real provider calls per provider per UTC day. ``limits`` missing a provider = no cap."""

    def __init__(self, inner: LLMClient, path: Path, limits: Mapping[str, int]) -> None:
        self._inner = inner
        self._store = _store(path)
        self._limits = dict(limits)

    def used_today(self, provider: str) -> int:
        with self._store.lock:
            row = self._store.db.execute(
                "SELECT requests FROM usage WHERE provider = ? AND day = ?",
                (provider, _today()),
            ).fetchone()
        return int(row[0]) if row else 0

    def complete(self, request: CompletionRequest) -> Completion:
        provider = request.provider
        limit = self._limits.get(provider)
        with self._store.lock:
            day = _today()
            row = self._store.db.execute(
                "SELECT requests FROM usage WHERE provider = ? AND day = ?", (provider, day)
            ).fetchone()
            used = int(row[0]) if row else 0
            if limit is not None and used >= limit:
                raise BudgetExceededError(
                    f"daily budget for '{provider}' reached ({used}/{limit} requests); "
                    "results are cached, so rerunning tomorrow continues where it stopped"
                )
            # Count the attempt before calling: failed calls also use the provider's quota.
            self._store.db.execute(
                "INSERT INTO usage VALUES (?, ?, 1) "
                "ON CONFLICT (provider, day) DO UPDATE SET requests = requests + 1",
                (provider, day),
            )
        return self._inner.complete(request)


def _today() -> str:
    return datetime.now(UTC).date().isoformat()
