"""E0 - end-to-end smoke test on the real corpus.

Asks a small fixed set of questions through the full pipeline (hybrid retrieval on the
``active`` index, Gemini via the cached gateway) and records, for each question, the answer,
citations, the retrieved sources with their vector/keyword ranks, and LLM usage.

This is a qualitative baseline, not a benchmark: it shows the system works end to end and
exposes failure cases worth turning into golden-set questions. Verdicts are human judgements
and live in ``annotations.md``, not in the generated results.

Run (API not needed; Postgres must be up and the index ingested):

    uv run python experiments/E0-smoke/run.py
"""

from __future__ import annotations

from pathlib import Path

from driftrag.config import get_settings
from driftrag.db.engine import make_engine
from driftrag.experiments.records import environment, index_snapshot, save_run
from driftrag.llm.factory import build_llm_client
from driftrag.rag.embeddings import E5Embedder
from driftrag.rag.generation import AnswerGenerator
from driftrag.rag.retrieval import HybridRetriever, Lang

REPO = Path(__file__).resolve().parents[2]
TOP_K = 5

QUESTIONS: list[tuple[str, Lang, str]] = [
    ("restart-deployment", "en", "How do I restart all the pods of a Deployment?"),
    ("probes", "en", "What is the difference between a liveness probe and a readiness probe?"),
    ("resource-limits", "en", "How can I limit how much CPU and memory a container can use?"),
    ("pod-fr", "fr", "Qu'est-ce qu'un Pod dans Kubernetes ?"),
    ("out-of-scope", "en", "What is the capital of France?"),
]


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    retriever = HybridRetriever(engine, embedder)
    generator = AnswerGenerator(
        retriever, build_llm_client(settings), model=settings.generator_model, top_k=TOP_K
    )

    results = []
    index_version_id: int | None = None
    for question_id, lang, question in QUESTIONS:
        answer = generator.answer(question, lang=lang)
        if answer.index_version is not None:
            index_version_id = answer.index_version.id
        completion = answer.completion
        results.append(
            {
                "id": question_id,
                "lang": lang,
                "question": question,
                "answer": answer.text,
                "refused": answer.refused,
                "prompt_version": answer.prompt_version,
                "citations": [c.__dict__ for c in answer.citations],
                "invalid_citations": answer.invalid_citations,
                "sources": [
                    {
                        "rank": rank,
                        "chunk_id": s.chunk_id,
                        "document_path": s.document_path,
                        "heading_path": s.heading_path,
                        "rrf_score": s.score,
                        "vector_rank": s.vector_rank,
                        "keyword_rank": s.keyword_rank,
                    }
                    for rank, s in enumerate(answer.sources, start=1)
                ],
                "usage": None
                if completion is None
                else {
                    "model": completion.model,
                    "input_tokens": completion.input_tokens,
                    "output_tokens": completion.output_tokens,
                    "cost_usd": completion.cost_usd,
                    "latency_ms": completion.latency_ms,
                    "cached": completion.cached,
                },
            }
        )
        print(f"{question_id}: refused={answer.refused} citations={len(answer.citations)}")

    with engine.connect() as conn:
        index = index_snapshot(conn, index_version_id) if index_version_id else None
    path = save_run(
        REPO / "experiments",
        "E0-smoke",
        "baseline",
        environment={**environment(REPO, settings), "index": index},
        config={"top_k": TOP_K, "alias": "active", "embedder": embedder.name},
        results=results,
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
