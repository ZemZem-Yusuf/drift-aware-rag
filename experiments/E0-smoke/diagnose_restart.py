"""E0 follow-up: why did "restart all the pods of a Deployment" miss `kubectl rollout restart`?

For the natural-language question and for a command-style query, records where the relevant
reference chunks rank in vector search, keyword search and the fused list (top 200 of each).
Retrieval only: no LLM call.

    uv run python experiments/E0-smoke/diagnose_restart.py
"""

from __future__ import annotations

from pathlib import Path

from driftrag.config import get_settings
from driftrag.db.engine import make_engine
from driftrag.experiments.records import environment, index_snapshot, save_run
from driftrag.rag.embeddings import E5Embedder
from driftrag.rag.retrieval import HybridRetriever

REPO = Path(__file__).resolve().parents[2]
CANDIDATES = 200
TARGET_DOCUMENTS = (
    "reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart.md",
    "reference/kubectl/quick-reference.md",
)
QUERIES = {
    "natural": "How do I restart all the pods of a Deployment?",
    "command": "kubectl rollout restart deployment",
}


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    retriever = HybridRetriever(engine, embedder, candidates=CANDIDATES)

    results = {}
    version_id = None
    for name, query in QUERIES.items():
        found = retriever.search(query, top_k=CANDIDATES)
        version_id = found.index_version.id
        targets = []
        for document in TARGET_DOCUMENTS:
            hits = [
                {
                    "fused_rank": rank,
                    "chunk_id": c.chunk_id,
                    "heading_path": c.heading_path,
                    "vector_rank": c.vector_rank,
                    "keyword_rank": c.keyword_rank,
                }
                for rank, c in enumerate(found.chunks, start=1)
                if c.document_path == document
            ]
            targets.append({"document": document, "best": hits[0] if hits else None})
        results[name] = {
            "query": query,
            "top5": [
                {
                    "document": c.document_path,
                    "heading_path": c.heading_path,
                    "vector_rank": c.vector_rank,
                    "keyword_rank": c.keyword_rank,
                }
                for c in found.chunks[:5]
            ],
            "targets": targets,
        }
        for t in targets:
            print(f"{name}: {t['document'].rsplit('/', 1)[-1]} -> {t['best']}")

    with engine.connect() as conn:
        index = index_snapshot(conn, version_id) if version_id else None
    path = save_run(
        REPO / "experiments",
        "E0-smoke",
        "diagnose-restart",
        environment={**environment(REPO, settings), "index": index},
        config={"candidates": CANDIDATES, "embedder": embedder.name},
        results=results,
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
