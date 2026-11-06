"""Embedding models behind one small interface (ADR-0004).

``Embedder`` is what the rest of the code depends on. Two implementations:

- ``HashingEmbedder``: deterministic feature hashing of word unigrams and bigrams into a fixed
  number of dimensions. No model download, no network, identical output on every machine, so
  CI and integration tests use it. It's also a useful lexical *baseline* in experiments: a
  semantic model that can't beat it isn't earning its cost.
- ``E5Embedder``: a small multilingual sentence-transformers model on CPU, for real runs.

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
from typing import Any, Protocol, cast, runtime_checkable

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


class _EncoderModel(Protocol):
    """The part of ``SentenceTransformer`` we use, so tests can inject a fake model."""

    def encode(
        self, sentences: list[str], *, batch_size: int, normalize_embeddings: bool
    ) -> Any: ...


class E5Embedder:
    """``intfloat/multilingual-e5-small`` on CPU: 384 dimensions, English and French (MIT license).

    E5 models were trained with prefixes: questions start with ``"query: "`` and indexed text with
    ``"passage: "``. Leaving them out measurably lowers retrieval quality, so they're added here
    and nowhere else.

    The revision is pinned so the same text always gets the same vector, weights are loaded from
    ``safetensors`` only (no pickle), and remote code is never executed (threat model T9).
    """

    MODEL_ID = "intfloat/multilingual-e5-small"
    REVISION = "614241f622f53c4eeff9890bdc4f31cfecc418b3"
    DIM = 384

    def __init__(self, *, batch_size: int = 32, model: _EncoderModel | None = None) -> None:
        self._batch_size = batch_size
        self._model = model

    @property
    def name(self) -> str:
        return f"{self.MODEL_ID}@{self.REVISION[:8]}"

    @property
    def dim(self) -> int:
        return self.DIM

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        return self._encode([f"passage: {text}" for text in texts])

    def embed_query(self, text: str) -> list[float]:
        return self._encode([f"query: {text}"])[0]

    def _encode(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        vectors = self._load().encode(texts, batch_size=self._batch_size, normalize_embeddings=True)
        return [[float(v) for v in row] for row in vectors]

    def _load(self) -> _EncoderModel:
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except ImportError as exc:  # pragma: no cover - depends on the install
                raise RuntimeError(
                    "the embeddings extra is not installed: run `uv sync --extra embeddings`"
                ) from exc
            model = SentenceTransformer(
                self.MODEL_ID,
                revision=self.REVISION,
                device="cpu",
                trust_remote_code=False,
                model_kwargs={"use_safetensors": True},
            )
            # Its encode() accepts more options than our protocol lists; the ones we use match.
            self._model = cast(_EncoderModel, model)
        return self._model


def to_pgvector(vector: Sequence[float]) -> str:
    """Text form accepted by pgvector's ``CAST(:v AS vector)``."""
    return "[" + ",".join(repr(float(v)) for v in vector) + "]"
