import os
from typing import Any

import pytest

from driftrag.rag.rerank import CrossEncoderReranker, KeywordOverlapReranker, Reranker


class FakePairModel:
    def __init__(self) -> None:
        self.calls: list[list[tuple[str, str]]] = []

    def predict(self, inputs: list[tuple[str, str]], *, batch_size: int) -> Any:
        self.calls.append(inputs)
        return [float(len(passage)) for _, passage in inputs]


def test_cross_encoder_scores_query_passage_pairs() -> None:
    fake = FakePairModel()
    reranker = CrossEncoderReranker(model=fake)
    assert isinstance(reranker, Reranker)
    assert reranker.score("q", ["a", "bbb"]) == [1.0, 3.0]
    assert fake.calls == [[("q", "a"), ("q", "bbb")]]
    assert reranker.name == "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1@1427fd65"


def test_empty_candidates_do_not_call_the_model() -> None:
    fake = FakePairModel()
    assert CrossEncoderReranker(model=fake).score("q", []) == []
    assert fake.calls == []


def test_keyword_overlap_reranker_is_deterministic() -> None:
    reranker = KeywordOverlapReranker()
    assert reranker.score("restart the pods", ["pods restart now", "storage"]) == [2.0, 0.0]


@pytest.mark.model
@pytest.mark.skipif(
    os.environ.get("DRIFTRAG_RUN_MODEL_TESTS") != "1",
    reason="downloads a 471 MB model; set DRIFTRAG_RUN_MODEL_TESTS=1",
)
def test_real_cross_encoder_ranks_the_answering_passage_first() -> None:
    scores = CrossEncoderReranker().score(
        "How do I trigger a restart of all the pods in a Deployment?",
        [
            "A PersistentVolume is a piece of storage in the cluster.",
            "kubectl rollout restart deployment/nginx restarts the pods of a deployment.",
            "Les Pods sont les plus petites unités déployables.",
        ],
    )
    assert scores[1] == max(scores)
