from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from driftrag.api.app import create_app, get_generator
from driftrag.llm.client import BudgetExceededError, FakeLLMClient, LLMError
from driftrag.rag.generation import AnswerGenerator
from driftrag.rag.retrieval import RetrievalError
from tests.unit.test_generation import CHUNKS, FakeRetriever


@pytest.fixture
def client_with() -> Iterator[object]:
    app = create_app()

    def make(generator: AnswerGenerator) -> TestClient:
        app.dependency_overrides[get_generator] = lambda: generator
        return TestClient(app)

    yield make
    app.dependency_overrides.clear()


def generator(llm: FakeLLMClient | None = None, chunks: list | None = None) -> AnswerGenerator:  # type: ignore[type-arg]
    return AnswerGenerator(
        FakeRetriever(CHUNKS if chunks is None else chunks),
        llm or FakeLLMClient(responder=lambda _: "Use kubectl rollout restart [1]."),
        model="gemini/flash",
    )


def test_ask_returns_answer_with_citations(client_with) -> None:  # type: ignore[no-untyped-def]
    response = client_with(generator()).post("/ask", json={"question": "How do I restart pods?"})
    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == "Use kubectl rollout restart [1]."
    assert body["refused"] is False
    assert body["citations"] == [
        {"source_id": 1, "document_path": "deploy.md", "heading_path": "Deployments > Restarting"}
    ]
    assert body["index_version"] == "k8s-1.33"
    assert body["prompt_version"] == "answer-v1"
    assert body["usage"]["model"] == "gemini/flash"


@pytest.mark.parametrize("question", ["", "a", "x" * 1001])
def test_question_size_is_limited(client_with, question: str) -> None:  # type: ignore[no-untyped-def]
    response = client_with(generator()).post("/ask", json={"question": question})
    assert response.status_code == 422


def test_unknown_language_is_rejected(client_with) -> None:  # type: ignore[no-untyped-def]
    response = client_with(generator()).post("/ask", json={"question": "pods?", "lang": "de"})
    assert response.status_code == 422


@pytest.mark.parametrize(
    ("error", "status_code"),
    [(BudgetExceededError("budget"), 429), (LLMError("boom: secret detail"), 502)],
)
def test_llm_errors_map_to_http_status(client_with, error: LLMError, status_code: int) -> None:  # type: ignore[no-untyped-def]
    response = client_with(generator(FakeLLMClient(errors=[error]))).post(
        "/ask", json={"question": "How do I restart pods?"}
    )
    assert response.status_code == status_code
    assert "secret detail" not in response.text  # provider error details aren't leaked


def test_missing_index_is_503(client_with) -> None:  # type: ignore[no-untyped-def]
    class Broken(FakeRetriever):
        def search(self, query, *, lang="en", top_k=5):  # type: ignore[no-untyped-def]
            raise RetrievalError("alias 'active' doesn't point to any index version")

    gen = AnswerGenerator(Broken([]), FakeLLMClient(), model="m")
    response = client_with(gen).post("/ask", json={"question": "pods?"})
    assert response.status_code == 503
