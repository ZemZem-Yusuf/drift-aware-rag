import math

import pytest

from driftrag.rag.embeddings import Embedder, HashingEmbedder, to_pgvector


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
