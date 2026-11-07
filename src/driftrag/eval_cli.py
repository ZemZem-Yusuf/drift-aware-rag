"""``driftrag-eval``: score the active index against the golden set and save the run.

    uv run driftrag-eval                      # verified items only (reportable numbers)
    uv run driftrag-eval --include-drafts     # dry run while the golden set is being reviewed

Saved under ``experiments/R1-retrieval/results/`` with the golden file's checksum and item
counts, so every number can be traced to the exact questions that produced it.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from evalkit.golden import GoldenItem, Status, load_golden, select
from evalkit.retrieval_eval import RetrievalReport, evaluate_retrieval
from evalkit.stats import bootstrap_ci, paired_difference_ci

REPO = Path(__file__).resolve().parents[2]
DEFAULT_GOLDEN = REPO / "golden" / "k8s-1.33.jsonl"


def _breakdown(report: RetrievalReport, field: str) -> dict[str, dict[str, object]]:
    groups: dict[str, list[float]] = {}
    for score in report.items:
        groups.setdefault(str(getattr(score, field)), []).append(score.recall_at_k)
    return {
        name: {"n": len(values), f"recall@{report.k}": str(bootstrap_ci(values))}
        for name, values in sorted(groups.items())
    }


def compare_with(baseline_path: Path, report: RetrievalReport) -> dict[str, Any]:
    """Paired differences (this run minus baseline) on the questions both runs scored."""
    saved = json.loads(baseline_path.read_text(encoding="utf-8"))
    before = {item["id"]: item for item in saved["results"]["items"]}
    pairs = [(before[s.id], s) for s in report.items if s.id in before]
    if not pairs:
        raise SystemExit("no common questions with the baseline run")
    differences = {}
    for metric in ("recall_at_k", "reciprocal_rank", "ndcg_at_k"):
        old = [float(b[metric]) for b, _ in pairs]
        new = [float(getattr(c, metric)) for _, c in pairs]
        differences[metric] = str(paired_difference_ci(old, new))
    return {
        "baseline_file": baseline_path.name,
        "n": len(pairs),
        "differences": differences,
        "improved": [c.id for b, c in pairs if c.recall_at_k > float(b["recall_at_k"])],
        "worse": [c.id for b, c in pairs if c.recall_at_k < float(b["recall_at_k"])],
    }


def main(argv: list[str] | None = None) -> None:
    from driftrag.config import get_settings
    from driftrag.db.engine import make_engine
    from driftrag.experiments.records import environment, index_snapshot, save_run
    from driftrag.rag.embeddings import E5Embedder
    from driftrag.rag.retrieval import HybridRetriever

    parser = argparse.ArgumentParser(description="Evaluate retrieval on the golden set.")
    parser.add_argument("--golden", type=Path, default=DEFAULT_GOLDEN)
    parser.add_argument("--k", type=int, default=5)
    parser.add_argument("--candidates", type=int, default=50)
    parser.add_argument("--include-drafts", action="store_true")
    parser.add_argument("--run-name", default="baseline")
    parser.add_argument("--alias", choices=["active", "canary"], default="active")
    parser.add_argument(
        "--baseline",
        type=Path,
        help="saved run to compare with, question by question (paired bootstrap)",
    )
    args = parser.parse_args(argv)

    all_items = load_golden(args.golden)
    statuses: tuple[Status, ...] = ("verified", "draft") if args.include_drafts else ("verified",)
    items: list[GoldenItem] = select(all_items, statuses=statuses)
    run_name = f"{args.run_name}-drafts" if args.include_drafts else args.run_name

    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    retriever = HybridRetriever(engine, embedder, alias=args.alias, candidates=args.candidates)
    version_ids: set[int] = set()

    def search(question: str, lang: str) -> list[tuple[str, str]]:
        result = retriever.search(question, lang="fr" if lang == "fr" else "en", top_k=10)
        version_ids.add(result.index_version.id)
        return [(c.document_path, c.heading_path) for c in result.chunks]

    reports = {k: evaluate_retrieval(items, search, k=k) for k in sorted({args.k, 10})}
    main_report = reports[args.k]

    print(f"{len(items)} questions ({'verified + drafts' if args.include_drafts else 'verified'})")
    for k, report in reports.items():
        print(f"  recall@{k}: {report.recall_at_k}")
    print(f"  MRR:       {main_report.mrr}")
    print(f"  nDCG@10:   {reports[10].ndcg_at_k}")
    comparison = compare_with(args.baseline, main_report) if args.baseline else None
    if comparison:
        print(f"  vs {comparison['baseline_file']} (paired, n={comparison['n']}):")
        for metric, value in comparison["differences"].items():
            print(f"    {metric}: {value}")
        print(f"    improved: {comparison['improved'] or 'none'}")
        print(f"    worse:    {comparison['worse'] or 'none'}")
    misses = [s for s in main_report.items if s.recall_at_k == 0]
    print(f"  no relevant source in top {args.k}: {', '.join(s.id for s in misses) or 'none'}")

    golden_bytes = args.golden.read_bytes()
    with engine.connect() as conn:
        index = index_snapshot(conn, next(iter(version_ids))) if version_ids else None
    path = save_run(
        REPO / "experiments",
        "R1-retrieval",
        run_name,
        environment={**environment(REPO, settings), "index": index},
        config={
            "golden_file": args.golden.name,
            "golden_sha256": hashlib.sha256(golden_bytes).hexdigest(),
            "golden_status_counts": dict(Counter(i.status for i in all_items)),
            "statuses_used": list(statuses),
            "k": args.k,
            "candidates": args.candidates,
            "embedder": embedder.name,
            "alias": args.alias,
        },
        results={
            "summary": {
                **{f"recall@{k}": str(r.recall_at_k) for k, r in reports.items()},
                "mrr": str(main_report.mrr),
                "ndcg@10": str(reports[10].ndcg_at_k),
                "comparison": comparison,
                "by_lang": _breakdown(main_report, "lang"),
                "by_category": _breakdown(main_report, "category"),
            },
            "items": [s.__dict__ for s in main_report.items],
        },
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
