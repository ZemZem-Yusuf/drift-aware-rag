"""H4: do fusion weights or candidate depth improve hybrid retrieval?

No re-indexing: the same ``active`` index, only retrieval parameters change.

Method (fixed before running, to limit tuning on the evaluation set):
- A small **pre-declared grid** of 8 settings (below); every setting is reported.
- Each setting is compared with the current baseline setting **on the same questions**
  (paired bootstrap of per-question differences).
- 7 comparisons are made, so besides the usual 95% interval a **Bonferroni-corrected**
  interval (confidence 1 - 0.05/7) is reported. A setting only counts as an improvement if
  the corrected interval for recall@5 excludes zero.
- Even then the winner is optimistic: it was chosen on these 28 questions. It must be
  confirmed on new questions before the gain is claimed.

    uv run python experiments/R1-retrieval/h4_fusion_sweep.py
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from driftrag.config import get_settings
from driftrag.db.engine import make_engine
from driftrag.experiments.records import environment, index_snapshot, save_run
from driftrag.rag.embeddings import E5Embedder
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
    candidates: int = 50
    vector_weight: float = 1.0
    keyword_weight: float = 1.0
    rrf_k: int = 60


GRID = [
    Setting("baseline"),  # the current production setting
    Setting("depth-100", candidates=100),
    Setting("depth-200", candidates=200),
    Setting("vector-x2", vector_weight=2.0),
    Setting("vector-x3", vector_weight=3.0),
    Setting("keyword-x2", keyword_weight=2.0),
    Setting("rrf-k-20", rrf_k=20),
    Setting("rrf-k-100", rrf_k=100),
]
COMPARISONS = len(GRID) - 1
CORRECTED_CONFIDENCE = 1 - 0.05 / COMPARISONS


def per_question(report: RetrievalReport, metric: str) -> list[float]:
    return [float(getattr(s, metric)) for s in report.items]


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    items = select(load_golden(GOLDEN))
    reports: dict[str, RetrievalReport] = {}
    version_id = None

    for setting in GRID:
        retriever = HybridRetriever(
            engine,
            embedder,
            candidates=setting.candidates,
            rrf_k=setting.rrf_k,
            weights=(setting.vector_weight, setting.keyword_weight),
        )

        def search(
            question: str, lang: str, retriever: HybridRetriever = retriever
        ) -> list[tuple[str, str]]:
            nonlocal version_id
            found = retriever.search(question, lang="fr" if lang == "fr" else "en", top_k=10)
            version_id = found.index_version.id
            return [(c.document_path, c.heading_path) for c in found.chunks]

        reports[setting.name] = evaluate_retrieval(items, search, k=K)

    base = reports["baseline"]
    rows = []
    for setting in GRID:
        report = reports[setting.name]
        row: dict[str, object] = {
            "setting": setting.__dict__,
            "recall@5": str(report.recall_at_k),
            "mrr": str(report.mrr),
            "ndcg@5": str(report.ndcg_at_k),
        }
        if setting.name != "baseline":
            old = per_question(base, "recall_at_k")
            new = per_question(report, "recall_at_k")
            row["recall@5_diff_95"] = str(paired_difference_ci(old, new))
            row["recall@5_diff_corrected"] = str(
                paired_difference_ci(old, new, confidence=CORRECTED_CONFIDENCE)
            )
            row["mrr_diff_95"] = str(
                paired_difference_ci(
                    per_question(base, "reciprocal_rank"), per_question(report, "reciprocal_rank")
                )
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
            f"{setting.name:11} recall@5 {report.recall_at_k}  MRR {report.mrr.mean:.3f}"
            + (f"  diff {row['recall@5_diff_95']}" if "recall@5_diff_95" in row else "")
        )

    with engine.connect() as conn:
        index = index_snapshot(conn, version_id) if version_id else None
    path = save_run(
        REPO / "experiments",
        "R1-retrieval",
        "h4-fusion-sweep",
        environment={**environment(REPO, settings), "index": index},
        config={
            "k": K,
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
