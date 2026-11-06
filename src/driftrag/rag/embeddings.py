"""Embedding models behind one small interface (ADR-0004).

``Embedder`` is what the rest of the code depends on. Two implementations:

- ``HashingEmbedder``: deterministic feature hashing of word unigrams and bigrams into a fixed
  number of dimensions. No model download, no network, identical output on every machine, so
  CI and integration tests use it. It's also a useful lexical *baseline* in experiments: a
  semantic model that can't beat it isn't earning its cost.
- A sentence-transformers model (multilingual, CPU) for real runs, added with the LLM gateway.

Every chunk and query stores the embedder's ``name`` (which includes its version), so drift
checks never compare vectors produced by different models by mistake (experiment E3).
"""

from __future__ import annotations

import hashlib
import itertools
import math
import re
import unicodedata
from collections.abc import Sequence
from typing import Protocol, runtime_checkable

_TOKEN = re.compile(r"\w+", re.UNICODE)


@runtime_checkable
class Embedder(Protocol):
    @property
    def name(self) -> str:
        """Model id including version, e.g. ``hashing-v1-256``. Stored with every vector."""
        ...

    @property
    def dim(self) -> int: ...

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]: ...

    def embed_query(self, text: str) -> list[float]: ...


class HashingEmbedder:
    """Deterministic bag-of-n-grams embedding using signed feature hashing, L2-normalised."""

    VERSION = 1

    def __init__(self, dim: int = 256) -> None:
        if not 8 <= dim <= 4096:
            raise ValueError("dim must be between 8 and 4096")
        self._dim = dim

    @property
    def name(self) -> str:
        return f"hashing-v{self.VERSION}-{self._dim}"

    @property
    def dim(self) -> int:
        return self._dim

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        normalised = unicodedata.normalize("NFKC", text).casefold()
        tokens = _TOKEN.findall(normalised)
        features = tokens + [f"{a} {b}" for a, b in itertools.pairwise(tokens)]
        vector = [0.0] * self._dim
        for feature in features:
            digest = hashlib.blake2b(feature.encode(), digest_size=8).digest()
            value = int.from_bytes(digest, "little")
            index = value % self._dim
            sign = 1.0 if (value >> 63) & 1 else -1.0  # signed hashing reduces collision bias
            vector[index] += sign
        norm = math.sqrt(sum(v * v for v in vector))
        return [v / norm for v in vector] if norm else vector


def to_pgvector(vector: Sequence[float]) -> str:
    """Text form accepted by pgvector's ``CAST(:v AS vector)``."""
    return "[" + ",".join(repr(float(v)) for v in vector) + "]"
