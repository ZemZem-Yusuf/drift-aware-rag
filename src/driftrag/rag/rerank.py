"""Rerankers: score how well each candidate passage answers the question (H2).

First-stage retrieval (vector + keyword, fused with RRF) is fast but judges the question and a
passage separately: an embedding of each, or shared words. A **cross-encoder** reads the
question and the passage *together* and outputs one relevance score, so it can see that
"restart all the pods of a Deployment" is answered by a page about `kubectl rollout restart`
even when the two share few words. It's too slow to run on the whole corpus, so it only
re-orders the top candidates of the first stage.

``CrossEncoderReranker`` uses ``cross-encoder/mmarco-mMiniLMv2-L12-H384-v1``: multilingual
(trained on mMARCO, which includes French), Apache-2.0, small enough for a laptop CPU. Same
loading rules as the embedder: pinned revision, safetensors only, no remote code.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any, Protocol, cast, runtime_checkable


@runtime_checkable
class Reranker(Protocol):
    @property
    def name(self) -> str: ...

    def score(self, query: str, passages: Sequence[str]) -> list[float]:
        """One relevance score per passage; higher means more relevant."""
        ...


class _PairModel(Protocol):
    def predict(self, inputs: list[tuple[str, str]], *, batch_size: int) -> Any: ...


class CrossEncoderReranker:
    MODEL_ID = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"
    REVISION = "1427fd652930e4ba29e8149678df786c240d8825"
    MAX_LENGTH = 512  # tokens per (question, passage) pair; longer passages are truncated

    def __init__(self, *, batch_size: int = 16, model: _PairModel | None = None) -> None:
        self._batch_size = batch_size
        self._model = model

    @property
    def name(self) -> str:
        return f"{self.MODEL_ID}@{self.REVISION[:8]}"

    def score(self, query: str, passages: Sequence[str]) -> list[float]:
        if not passages:
            return []
        scores = self._load().predict(
            [(query, passage) for passage in passages], batch_size=self._batch_size
        )
        return [float(s) for s in scores]

    def _load(self) -> _PairModel:
        if self._model is None:
            try:
                from sentence_transformers import CrossEncoder
            except ImportError as exc:  # pragma: no cover - depends on the install
                raise RuntimeError(
                    "the embeddings extra is not installed: run `uv sync --extra embeddings`"
                ) from exc
            model = CrossEncoder(
                self.MODEL_ID,
                revision=self.REVISION,
                device="cpu",
                trust_remote_code=False,
                max_length=self.MAX_LENGTH,
                model_kwargs={"use_safetensors": True},
            )
            self._model = cast(_PairModel, model)
        return self._model


class KeywordOverlapReranker:
    """Deterministic stand-in for tests: scores passages by shared lowercase words."""

    name = "keyword-overlap-v1"

    def score(self, query: str, passages: Sequence[str]) -> list[float]:
        words = set(query.lower().split())
        return [float(len(words & set(p.lower().split()))) for p in passages]
