"""H2: does a cross-encoder reranker improve retrieval, and what does it cost in latency?

Same ``active`` index; the first stage is unchanged (50 candidates per search, RRF k=60, 1:1).
The reranker re-orders the top fused candidates.

Method (fixed before running):
- Pre-declared settings: no reranking (baseline); rerank the top 30 with "section path +
  text" as the passage; the same with text only; rerank the top 50 with section path + text.
- Paired bootstrap against the baseline on the same questions; 3 comparisons, so a
  Bonferroni-corrected interval (confidence 1 - 0.05/3) is reported too.
- Retrieval latency per query (p50/p95), measured after one warm-up query so model loading
  isn't counted. CPU only.

    uv run python experiments/R1-retrieval/h2_rerank.py
"""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
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


@dataclass(frozen=True)
class Setting:
    name: str
    rerank: bool = False
    depth: int = 30
    with_heading: bool = True


GRID = [
    Setting("baseline"),
    Setting("rerank-30", rerank=True, depth=30, with_heading=True),
    Setting("rerank-30-text-only", rerank=True, depth=30, with_heading=False),
    Setting("rerank-50", rerank=True, depth=50, with_heading=True),
]
COMPARISONS = len(GRID) - 1
CORRECTED_CONFIDENCE = 1 - 0.05 / COMPARISONS


def scores(report: RetrievalReport, metric: str) -> list[float]:
    return [float(getattr(s, metric)) for s in report.items]


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    reranker = CrossEncoderReranker()
    items = select(load_golden(GOLDEN))
    reports: dict[str, RetrievalReport] = {}
    latencies: dict[str, list[float]] = {}
    version_id = None

    for setting in GRID:
        retriever = HybridRetriever(
            engine,
            embedder,
            reranker=reranker if setting.rerank else None,
            rerank_depth=setting.depth,
            rerank_with_heading=setting.with_heading,
        )
        retriever.search("warm-up query about pods", top_k=K)  # load models, warm caches
        timings: list[float] = []

        def search(
            question: str,
            lang: str,
            retriever: HybridRetriever = retriever,
            timings: list[float] = timings,
        ) -> list[tuple[str, str]]:
            nonlocal version_id
            started = time.perf_counter()
            found = retriever.search(question, lang="fr" if lang == "fr" else "en", top_k=10)
            timings.append((time.perf_counter() - started) * 1000)
            version_id = found.index_version.id
            return [(c.document_path, c.heading_path) for c in found.chunks]

        reports[setting.name] = evaluate_retrieval(items, search, k=K)
        latencies[setting.name] = timings

    base = reports["baseline"]
    rows = []
    for setting in GRID:
        report = reports[setting.name]
        ms = sorted(latencies[setting.name])
        row: dict[str, object] = {
            "setting": setting.__dict__,
            "recall@5": str(report.recall_at_k),
            "mrr": str(report.mrr),
            "ndcg@5": str(report.ndcg_at_k),
            "latency_ms": {
                "p50": round(statistics.median(ms), 1),
                "p95": round(ms[int(0.95 * (len(ms) - 1))], 1),
                "mean": round(statistics.fmean(ms), 1),
            },
        }
        if setting.name != "baseline":
            for metric, label in (("recall_at_k", "recall@5"), ("reciprocal_rank", "mrr")):
                old, new = scores(base, metric), scores(report, metric)
                row[f"{label}_diff_95"] = str(paired_difference_ci(old, new))
                row[f"{label}_diff_corrected"] = str(
                    paired_difference_ci(old, new, confidence=CORRECTED_CONFIDENCE)
                )
            row["improved"] = [
                n.id
                for o, n in zip(base.items, report.items, strict=True)
                if n.recall_at_k > o.recall_at_k
            ]
            row["worse"] = [
                n.id
                for o, n in zip(base.items, report.items, strict=True)
                if n.recall_at_k < o.recall_at_k
            ]
        rows.append(row)
        print(
            f"{setting.name:20} recall@5 {report.recall_at_k}  MRR {report.mrr.mean:.3f}  "
            f"p50 {row['latency_ms']['p50']} ms"  # type: ignore[index]
        )

    with engine.connect() as conn:
        index = index_snapshot(conn, version_id) if version_id else None
    path = save_run(
        REPO / "experiments",
        "R1-retrieval",
        "h2-rerank",
        environment={**environment(REPO, settings), "index": index},
        config={
            "k": K,
            "first_stage": {"candidates": 50, "rrf_k": 60, "weights": [1, 1]},
            "reranker": reranker.name,
            "grid": [s.__dict__ for s in GRID],
            "comparisons": COMPARISONS,
            "corrected_confidence": CORRECTED_CONFIDENCE,
            "questions": len(items),
        },
        results=rows,
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
