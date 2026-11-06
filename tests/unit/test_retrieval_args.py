import pytest
from sqlalchemy import create_engine

from driftrag.rag.embeddings import HashingEmbedder
from driftrag.rag.retrieval import HybridRetriever

# No connection is opened: argument checks happen before any database access.
ENGINE = create_engine("postgresql+psycopg://user:pw@127.0.0.1:1/none")


def test_candidates_must_be_positive() -> None:
    with pytest.raises(ValueError, match="candidates"):
        HybridRetriever(ENGINE, HashingEmbedder(), candidates=0)


@pytest.mark.parametrize(("query", "top_k", "message"), [(" ", 5, "query"), ("pods", 0, "top_k")])
def test_invalid_search_arguments(query: str, top_k: int, message: str) -> None:
    retriever = HybridRetriever(ENGINE, HashingEmbedder())
    with pytest.raises(ValueError, match=message):
        retriever.search(query, top_k=top_k)
