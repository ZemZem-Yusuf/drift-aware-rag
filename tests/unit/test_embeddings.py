import math
import os

import pytest

from driftrag.rag.embeddings import E5Embedder, Embedder, HashingEmbedder, to_pgvector


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b, strict=True))


def test_hashing_embedder_satisfies_the_interface() -> None:
    embedder = HashingEmbedder(dim=64)
    assert isinstance(embedder, Embedder)
    assert embedder.name == "hashing-v1-64"
    assert embedder.dim == 64


def test_vectors_are_normalised_and_deterministic() -> None:
    embedder = HashingEmbedder(dim=128)
    first = embedder.embed_query("How do I restart a Deployment?")
    second = HashingEmbedder(dim=128).embed_query("How do I restart a Deployment?")
    assert first == second
    assert math.isclose(math.sqrt(sum(v * v for v in first)), 1.0)
    assert len(first) == 128


def test_similar_texts_are_closer_than_unrelated_ones() -> None:
    embedder = HashingEmbedder(dim=512)
    query = embedder.embed_query("restart a deployment with kubectl rollout restart")
    related, unrelated = embedder.embed_documents(
        [
            "Use kubectl rollout restart to restart a Deployment.",
            "Persistent volumes provide storage that outlives Pods.",
        ]
    )
    assert cosine(query, related) > cosine(query, unrelated)


def test_case_and_unicode_forms_do_not_matter() -> None:
    embedder = HashingEmbedder(dim=64)
    assert embedder.embed_query("Conteneurs") == embedder.embed_query("conteneurs")
    assert embedder.embed_query("ﬁle") == embedder.embed_query("file")  # NFKC ligature


def test_empty_text_gives_zero_vector() -> None:
    assert HashingEmbedder(dim=16).embed_query("") == [0.0] * 16


@pytest.mark.parametrize("dim", [0, 7, 5000])
def test_dimension_bounds(dim: int) -> None:
    with pytest.raises(ValueError, match="dim"):
        HashingEmbedder(dim=dim)


def test_to_pgvector_format() -> None:
    assert to_pgvector([1, 0.5, -2]) == "[1.0,0.5,-2.0]"


class FakeEncoder:
    """Records what the embedder sends to the model; returns one fixed vector per input."""

    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def encode(
        self, sentences: list[str], *, batch_size: int, normalize_embeddings: bool
    ) -> list[list[float]]:
        assert normalize_embeddings
        self.calls.append(sentences)
        return [[0.6, 0.8] for _ in sentences]


def test_e5_adds_query_and_passage_prefixes() -> None:
    fake = FakeEncoder()
    embedder = E5Embedder(model=fake)

    embedder.embed_documents(["Pods are small.", "Services expose apps."])
    vector = embedder.embed_query("what is a pod?")

    assert fake.calls == [
        ["passage: Pods are small.", "passage: Services expose apps."],
        ["query: what is a pod?"],
    ]
    assert vector == [0.6, 0.8]


def test_e5_name_pins_the_revision() -> None:
    embedder = E5Embedder(model=FakeEncoder())
    assert isinstance(embedder, Embedder)
    assert embedder.name == "intfloat/multilingual-e5-small@614241f6"
    assert embedder.dim == 384


def test_e5_empty_batch_does_not_call_the_model() -> None:
    fake = FakeEncoder()
    assert E5Embedder(model=fake).embed_documents([]) == []
    assert fake.calls == []


@pytest.mark.model
@pytest.mark.skipif(
    os.environ.get("DRIFTRAG_RUN_MODEL_TESTS") != "1",
    reason="downloads a 470 MB model; set DRIFTRAG_RUN_MODEL_TESTS=1",
)
def test_real_e5_model_understands_english_and_french() -> None:
    embedder = E5Embedder()
    query_en = embedder.embed_query("How do I restart the pods of a deployment?")
    query_fr = embedder.embed_query("Comment redémarrer les pods de mon déploiement ?")
    relevant, unrelated = embedder.embed_documents(
        [
            "Use kubectl rollout restart deployment/my-app to restart all Pods of a Deployment.",
            "A PersistentVolume is a piece of storage in the cluster.",
        ]
    )
    assert len(relevant) == 384
    assert math.isclose(math.sqrt(sum(v * v for v in relevant)), 1.0, rel_tol=1e-5)
    assert cosine(query_en, relevant) > cosine(query_en, unrelated)
    assert cosine(query_fr, relevant) > cosine(query_fr, unrelated)  # cross-lingual
