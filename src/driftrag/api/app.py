"""FastAPI application factory."""

from functools import lru_cache
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from driftrag import __version__
from driftrag.config import get_settings
from driftrag.llm.client import BudgetExceededError, LLMError
from driftrag.rag.generation import AnswerGenerator
from driftrag.rag.retrieval import RetrievalError


class HealthResponse(BaseModel):
    status: str
    version: str
    env: str


class AskRequest(BaseModel):
    # Size limits are part of the abuse/cost controls (threat model T13).
    question: str = Field(min_length=3, max_length=1000)
    lang: Literal["en", "fr"] = "en"


class CitationOut(BaseModel):
    source_id: int
    document_path: str
    heading_path: str


class UsageOut(BaseModel):
    model: str | None
    input_tokens: int
    output_tokens: int
    cost_usd: float | None
    latency_ms: float
    cached: bool


class AskResponse(BaseModel):
    answer: str
    refused: bool
    citations: list[CitationOut]
    invalid_citations: list[int]
    index_version: str | None
    prompt_version: str
    usage: UsageOut


@lru_cache(maxsize=1)
def get_generator() -> AnswerGenerator:
    """Build the real pipeline once per process (database, E5 model, LLM gateway)."""
    from driftrag.db.engine import make_engine
    from driftrag.llm.factory import build_llm_client
    from driftrag.rag.embeddings import E5Embedder
    from driftrag.rag.retrieval import HybridRetriever

    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    retriever = HybridRetriever(engine, E5Embedder())
    return AnswerGenerator(retriever, build_llm_client(settings), model=settings.generator_model)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="Drift-Aware RAG", version=__version__)

    @app.get("/health", response_model=HealthResponse, tags=["ops"])
    def health() -> HealthResponse:
        return HealthResponse(status="ok", version=__version__, env=settings.env)

    @app.post("/ask", response_model=AskResponse, tags=["rag"])
    def ask(
        body: AskRequest, generator: Annotated[AnswerGenerator, Depends(get_generator)]
    ) -> AskResponse:
        try:
            answer = generator.answer(body.question, lang=body.lang)
        except RetrievalError as exc:
            raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(exc)) from exc
        except BudgetExceededError as exc:
            raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, str(exc)) from exc
        except LLMError as exc:
            raise HTTPException(status.HTTP_502_BAD_GATEWAY, "the language model failed") from exc

        completion = answer.completion
        return AskResponse(
            answer=answer.text,
            refused=answer.refused,
            citations=[
                CitationOut(
                    source_id=c.source_id,
                    document_path=c.document_path,
                    heading_path=c.heading_path,
                )
                for c in answer.citations
            ],
            invalid_citations=answer.invalid_citations,
            index_version=answer.index_version.name if answer.index_version else None,
            prompt_version=answer.prompt_version,
            usage=UsageOut(
                model=completion.model if completion else None,
                input_tokens=completion.input_tokens if completion else 0,
                output_tokens=completion.output_tokens if completion else 0,
                cost_usd=completion.cost_usd if completion else 0.0,
                latency_ms=completion.latency_ms if completion else 0.0,
                cached=completion.cached if completion else False,
            ),
        )

    return app


app = create_app()
