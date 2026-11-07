"""E4 step 1: answer every verified golden question with the production pipeline.

Pipeline as it stands (see README): ``active`` index, default hybrid retrieval, no reranker,
top 5 sources, prompt ``answer-v1``, the configured generator at temperature 0. The results
file keeps the sources exactly as the model saw them, so labellers and judges rate the answer
against the same text.

Free-tier friendly: real calls are paced, and answers are cached, so if the provider's daily
quota runs out the script stops without saving and a rerun (e.g. the next day) continues where
it stopped, without repeating calls.

    uv run python experiments/E4-judge/generate_answers.py
"""

from __future__ import annotations

import statistics
import sys
import time
from pathlib import Path

from driftrag.config import get_settings
from driftrag.db.engine import make_engine
from driftrag.experiments.records import environment, index_snapshot, save_run
from driftrag.llm.client import RetryableLLMError
from driftrag.llm.factory import build_llm_client
from driftrag.rag.embeddings import E5Embedder
from driftrag.rag.generation import PROMPT_VERSION, Answer, AnswerGenerator
from driftrag.rag.retrieval import HybridRetriever, Lang
from evalkit.golden import GoldenItem, load_golden, select

REPO = Path(__file__).resolve().parents[2]
GOLDEN = REPO / "golden" / "k8s-1.33.jsonl"
TOP_K = 5
PACE_S = 6.5  # between real provider calls: stays under a 10 requests/minute free-tier limit
RATE_LIMIT_WAIT_S = 65


def record(item: GoldenItem, answer: Answer) -> dict[str, object]:
    cited = {c.source_id for c in answer.citations}
    completion = answer.completion
    return {
        "id": item.id,
        "lang": item.lang,
        "category": item.category,
        "question": item.question,
        "reference_answer": item.reference_answer,
        "answer": answer.text,
        "refused": answer.refused,
        "citations": sorted(cited),
        "invalid_citations": answer.invalid_citations,
        "sources": [
            {
                "number": n,
                "document": chunk.document_path,
                "section": chunk.heading_path,
                "content": chunk.content,
                "cited": n in cited,
            }
            for n, chunk in enumerate(answer.sources, start=1)
        ],
        "model": completion.model if completion else None,
        "input_tokens": completion.input_tokens if completion else 0,
        "output_tokens": completion.output_tokens if completion else 0,
        "latency_ms": round(completion.latency_ms, 1) if completion else 0.0,
        "cached": completion.cached if completion else False,
    }


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    generator = AnswerGenerator(
        HybridRetriever(engine, E5Embedder()),
        build_llm_client(settings),
        model=settings.generator_model,
        top_k=TOP_K,
    )
    items = select(load_golden(GOLDEN), include_out_of_scope=True)
    rows: list[dict[str, object]] = []
    version_ids: set[int] = set()
    real_calls = 0

    for number, item in enumerate(items, start=1):
        lang: Lang = "fr" if item.lang == "fr" else "en"
        try:
            answer = generator.answer(item.question, lang=lang)
        except RetryableLLMError as first:
            print(f"{item.id}: {first}; waiting {RATE_LIMIT_WAIT_S} s and retrying once")
            time.sleep(RATE_LIMIT_WAIT_S)
            try:
                answer = generator.answer(item.question, lang=lang)
            except RetryableLLMError as second:
                print(
                    f"stopped at {number - 1} of {len(items)} answers: {second}. Nothing saved; "
                    "answers so far are cached, so rerunning later continues from here."
                )
                sys.exit(2)
        if answer.index_version is not None:
            version_ids.add(answer.index_version.id)
        rows.append(record(item, answer))
        is_real = answer.completion is not None and not answer.completion.cached
        real_calls += is_real
        status = "refused" if answer.refused else f"{len(answer.citations)} citations"
        print(f"[{number}/{len(items)}] {item.id}: {status}{'' if is_real else ' (cached)'}")
        if is_real:
            time.sleep(PACE_S)

    if len(version_ids) != 1:
        raise RuntimeError(f"expected one index version, got {sorted(version_ids)}")
    in_scope = [r for r in rows if r["category"] != "out-of-scope"]
    answered = [r for r in rows if not r["refused"]]
    summary = {
        "questions": len(rows),
        "answered": len(answered),
        "refused_in_scope": sum(bool(r["refused"]) for r in in_scope),
        "refused_out_of_scope": sum(
            bool(r["refused"]) for r in rows if r["category"] == "out-of-scope"
        ),
        "out_of_scope_total": len(rows) - len(in_scope),
        "answers_with_invalid_citations": sum(bool(r["invalid_citations"]) for r in rows),
        "answers_without_citations": sum(not r["citations"] for r in answered),
        "median_output_tokens": statistics.median(int(str(r["output_tokens"])) for r in answered)
        if answered
        else None,
        "real_calls_this_run": real_calls,
    }
    print(summary)

    with engine.connect() as conn:
        index = index_snapshot(conn, version_ids.pop())
    path = save_run(
        REPO / "experiments",
        "E4-judge",
        "answers",
        environment={**environment(REPO, settings), "index": index},
        config={
            "alias": "active",
            "top_k": TOP_K,
            "reranker": None,
            "prompt_version": PROMPT_VERSION,
            "generator_model": settings.generator_model,
            "temperature": 0.0,
            "golden": GOLDEN.relative_to(REPO).as_posix(),
        },
        results={"summary": summary, "answers": rows},
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
