"""H2 held-out check: does the reranker's gain hold on questions written after H2 was designed?

The first H2 run (28 questions, index 3) chose "rerank the top 30, section path + text" as the
setting to watch. The 57 questions added for golden set v2 didn't exist then, so they are a
fresh sample for that one setting.

Method (fixed before seeing the H2 re-run on 85 questions):
- Questions: the 57 verified retrieval questions that are not among the original 28 (ids
  listed below, taken from golden/k8s-1.33.jsonl at commit 43f0284).
- One comparison only, so a plain 95% paired bootstrap interval: rerank-30 minus baseline,
  on recall@5 and MRR. Same ``active`` index and first stage as h2_rerank.py.
- No latency numbers here; h2_rerank.py measures latency on a quiet machine.

    uv run python experiments/R1-retrieval/h2_heldout.py
"""

from __future__ import annotations

from pathlib import Path

from driftrag.config import get_settings
from driftrag.db.engine import make_engine
from driftrag.experiments.records import environment, index_snapshot, save_run
from driftrag.rag.embeddings import E5Embedder
from driftrag.rag.rerank import CrossEncoderReranker
from driftrag.rag.retrieval import HybridRetriever
from evalkit.golden import load_golden, select
from evalkit.retrieval_eval import RetrievalReport, evaluate_retrieval
from evalkit.stats import paired_difference_ci

REPO = Path(__file__).resolve().parents[2]
GOLDEN = REPO / "golden" / "k8s-1.33.jsonl"
K = 5
RERANK_DEPTH = 30

ORIGINAL_28 = frozenset(
    {
        "configmap-env", "crashloop", "cronjob-nightly", "daemonset-agent", "drain-node",
        "fr-labels-selectors", "fr-pod-multi-container", "fr-rollback", "fr-scale",
        "fr-service-types", "hpa-cpu", "image-pull-policy", "ingress-vs-service",
        "init-container-setup", "namespaces-when", "netpol-default-deny", "pdb-keep-replicas",
        "pod-pending", "probes-difference", "pvc-request-storage", "rbac-role-clusterrole",
        "resource-limits", "restart-deployment", "rollback-deployment", "scale-deployment",
        "secret-encryption", "service-types", "taint-dedicated-node",
    }
)  # fmt: skip


def scores(report: RetrievalReport, metric: str) -> list[float]:
    return [float(getattr(s, metric)) for s in report.items]


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    reranker = CrossEncoderReranker()
    items = [i for i in select(load_golden(GOLDEN)) if i.id not in ORIGINAL_28]
    version_ids: set[int] = set()

    def run(retriever: HybridRetriever) -> RetrievalReport:
        def search(question: str, lang: str) -> list[tuple[str, str]]:
            found = retriever.search(question, lang="fr" if lang == "fr" else "en", top_k=10)
            version_ids.add(found.index_version.id)
            return [(c.document_path, c.heading_path) for c in found.chunks]

        return evaluate_retrieval(items, search, k=K)

    base = run(HybridRetriever(engine, embedder))
    rerank = run(
        HybridRetriever(
            engine, embedder, reranker=reranker, rerank_depth=RERANK_DEPTH, rerank_with_heading=True
        )
    )
    if len(version_ids) != 1:
        raise RuntimeError(f"the active index changed during the run: {sorted(version_ids)}")

    results: dict[str, object] = {
        "questions": len(items),
        "baseline": {"recall@5": str(base.recall_at_k), "mrr": str(base.mrr)},
        "rerank-30": {"recall@5": str(rerank.recall_at_k), "mrr": str(rerank.mrr)},
    }
    for metric, label in (("recall_at_k", "recall@5"), ("reciprocal_rank", "mrr")):
        diff = paired_difference_ci(scores(base, metric), scores(rerank, metric))
        results[f"{label}_diff_95"] = str(diff)
        print(f"{label:9} diff {diff}")
    results["improved"] = [
        n.id for o, n in zip(base.items, rerank.items, strict=True) if n.recall_at_k > o.recall_at_k
    ]
    results["worse"] = [
        n.id for o, n in zip(base.items, rerank.items, strict=True) if n.recall_at_k < o.recall_at_k
    ]
    print(f"baseline  recall@5 {base.recall_at_k}  MRR {base.mrr.mean:.3f}")
    print(f"rerank-30 recall@5 {rerank.recall_at_k}  MRR {rerank.mrr.mean:.3f}")
    print("improved", results["improved"], "| worse", results["worse"])

    with engine.connect() as conn:
        index = index_snapshot(conn, version_ids.pop())
    path = save_run(
        REPO / "experiments",
        "R1-retrieval",
        "h2-heldout",
        environment={**environment(REPO, settings), "index": index},
        config={
            "k": K,
            "first_stage": {"candidates": 50, "rrf_k": 60, "weights": [1, 1]},
            "reranker": reranker.name,
            "rerank_depth": RERANK_DEPTH,
            "rerank_with_heading": True,
            "excluded_original_ids": sorted(ORIGINAL_28),
            "questions": len(items),
        },
        results=results,
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
