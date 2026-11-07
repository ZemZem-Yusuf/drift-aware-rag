"""Score a retriever against a golden set with recall@k, reciprocal rank and nDCG@k.

The retriever is any callable ``search(question, lang) -> ranked list of (document,
heading_path)``, so evalkit stays independent of how retrieval is implemented.

Each retrieved chunk is mapped to the golden item's relevant-section key it matches (or to a
unique "miss" id), then the standard metrics from ``evalkit.metrics`` are applied. Several
chunks of the same relevant section count once, keeping their slots (see metrics docs).
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from evalkit.golden import GoldenItem
from evalkit.metrics import ndcg_at_k, recall_at_k, reciprocal_rank
from evalkit.stats import Estimate, bootstrap_ci

Retrieved = Sequence[tuple[str, str]]  # (document, heading_path), best first
SearchFn = Callable[[str, str], Retrieved]


@dataclass(frozen=True)
class ItemScore:
    id: str
    lang: str
    category: str
    recall_at_k: float
    reciprocal_rank: float
    ndcg_at_k: float
    first_hit_rank: int | None
    retrieved: list[tuple[str, str]]


@dataclass(frozen=True)
class RetrievalReport:
    k: int
    items: list[ItemScore]
    recall_at_k: Estimate
    mrr: Estimate
    ndcg_at_k: Estimate


def as_ids(item: GoldenItem, retrieved: Retrieved) -> list[str]:
    ids = []
    for position, (document, heading) in enumerate(retrieved):
        keys = item.relevant_keys_for(document, heading)
        ids.append(keys[0] if keys else f"miss:{position}")
    return ids


def score_item(item: GoldenItem, retrieved: Retrieved, k: int) -> ItemScore:
    ids = as_ids(item, retrieved)
    relevant = [r.key for r in item.relevant]
    first_hit = next((p for p, i in enumerate(ids, start=1) if not i.startswith("miss:")), None)
    return ItemScore(
        id=item.id,
        lang=item.lang,
        category=item.category,
        recall_at_k=recall_at_k(ids, relevant, k),
        reciprocal_rank=reciprocal_rank(ids, relevant),
        ndcg_at_k=ndcg_at_k(ids, relevant, k),
        first_hit_rank=first_hit,
        retrieved=list(retrieved),
    )


def evaluate_retrieval(
    items: Sequence[GoldenItem], search: SearchFn, *, k: int = 5, seed: int = 0
) -> RetrievalReport:
    scored = [score_item(item, search(item.question, item.lang), k) for item in items]
    if not scored:
        raise ValueError("no golden items to evaluate (are any marked 'verified'?)")
    return RetrievalReport(
        k=k,
        items=scored,
        recall_at_k=bootstrap_ci([s.recall_at_k for s in scored], seed=seed),
        mrr=bootstrap_ci([s.reciprocal_rank for s in scored], seed=seed),
        ndcg_at_k=bootstrap_ci([s.ndcg_at_k for s in scored], seed=seed),
    )
