"""H1 follow-up: for the vocabulary-gap misses, did embedding headings move the right page up?

Compares the *vector* rank (top 200) of the relevant document for a few missed questions on
``active`` (content only) and ``canary`` (heading + content). Retrieval only, no LLM call.

    uv run python experiments/R1-retrieval/h1_vector_ranks.py
"""

from __future__ import annotations

from pathlib import Path

from driftrag.config import get_settings
from driftrag.db.engine import make_engine
from driftrag.experiments.records import environment, save_run
from driftrag.rag.embeddings import E5Embedder
from driftrag.rag.retrieval import HybridRetriever

REPO = Path(__file__).resolve().parents[2]
CASES = {
    "restart-deployment": (
        "How do I trigger a restart of all the pods in a Deployment?",
        "reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart.md",
    ),
    "taint-dedicated-node": (
        "How can I keep ordinary pods from being scheduled on a particular node?",
        "concepts/scheduling-eviction/taint-and-toleration.md",
    ),
    "daemonset-agent": (
        "How do I run exactly one copy of a log collector on every node of the cluster?",
        "concepts/workloads/controllers/daemonset.md",
    ),
    "hpa-cpu": (
        "How can Kubernetes add more pods automatically when CPU usage goes up?",
        "tasks/run-application/horizontal-pod-autoscale.md",
    ),
}


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    results: dict[str, dict[str, object]] = {}
    for alias in ("active", "canary"):
        retriever = HybridRetriever(engine, embedder, alias=alias, candidates=200)
        for case, (question, document) in CASES.items():
            found = retriever.search(question, top_k=200)
            hits = [c for c in found.chunks if c.document_path == document]
            best_vector = min((c.vector_rank for c in hits if c.vector_rank), default=None)
            best_keyword = min((c.keyword_rank for c in hits if c.keyword_rank), default=None)
            results.setdefault(case, {})[alias] = {
                "index": found.index_version.name,
                "best_vector_rank": best_vector,
                "best_keyword_rank": best_keyword,
            }
            print(f"{case:22} [{alias}] vector={best_vector} keyword={best_keyword}")
    path = save_run(
        REPO / "experiments",
        "R1-retrieval",
        "h1-vector-ranks",
        environment=environment(REPO, settings),
        config={"candidates": 200, "aliases": ["active", "canary"]},
        results=results,
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
