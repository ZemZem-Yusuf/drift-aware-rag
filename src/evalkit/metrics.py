"""Retrieval metrics with binary relevance (a chunk is either relevant to a question or not).

For each golden-set question we know the ids of the relevant chunks. Given the ranked list the
retriever returned, these metrics answer different questions:

- ``recall_at_k``: did we find the relevant chunks at all within the top k?
  (What the generator can possibly use.)
- ``reciprocal_rank``: how high is the *first* relevant chunk? (1 / its rank.)
  Averaged over questions it's MRR.
- ``ndcg_at_k``: are *all* relevant chunks near the top? Each hit is discounted by
  ``log2(rank + 1)``, and the sum is divided by the best possible sum (ideal ordering).

Duplicate ids in ``retrieved`` count only once, at their first position, but every repeat still
takes up its slot: a retriever must not earn credit twice for the same chunk, and wasting a
position must not move later results up.

Invalid input raises ``ValueError`` with a message that mentions ``k`` or ``relevant``.
"""

import math
from collections.abc import Collection, Sequence


def _relevant_set(relevant: Collection[str]) -> frozenset[str]:
    """Validate and freeze the relevant ids. Recall and nDCG are undefined without any."""
    relevant_ids = frozenset(relevant)
    if not relevant_ids:
        raise ValueError("relevant must contain at least one id")
    return relevant_ids


def _check_k(k: int) -> None:
    if k <= 0:
        raise ValueError(f"k must be a positive integer, got {k}")


def recall_at_k(retrieved: Sequence[str], relevant: Collection[str], k: int) -> float:
    """Share of relevant ids found in the first ``k`` retrieved ids.

    Raises:
        ValueError: if ``k <= 0`` or ``relevant`` is empty (recall is undefined).
    """
    _check_k(k)
    relevant_ids = _relevant_set(relevant)
    found = relevant_ids.intersection(retrieved[:k])  # a set, so duplicates count once
    return len(found) / len(relevant_ids)


def reciprocal_rank(retrieved: Sequence[str], relevant: Collection[str]) -> float:
    """``1 / rank`` of the first relevant id (rank is 1-based), or ``0.0`` if none is retrieved.

    Duplicates need no special handling: the first time a relevant id appears is, by
    definition, its first position, and earlier duplicates still occupy their slots.

    Raises:
        ValueError: if ``relevant`` is empty.
    """
    relevant_ids = _relevant_set(relevant)
    for rank, doc_id in enumerate(retrieved, start=1):
        if doc_id in relevant_ids:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: Sequence[str], relevant: Collection[str], k: int) -> float:
    """Normalised discounted cumulative gain at ``k``, with binary relevance.

    ``DCG  = sum over the first k positions i (1-based) of rel_i / log2(i + 1)``
    ``IDCG = sum for i = 1 .. min(k, len(relevant)) of 1 / log2(i + 1)``
    ``nDCG = DCG / IDCG``

    Raises:
        ValueError: if ``k <= 0`` or ``relevant`` is empty.
    """
    _check_k(k)
    relevant_ids = _relevant_set(relevant)

    dcg = 0.0
    seen: set[str] = set()
    for rank, doc_id in enumerate(retrieved[:k], start=1):
        if doc_id in relevant_ids and doc_id not in seen:
            dcg += 1.0 / math.log2(rank + 1)
        seen.add(doc_id)  # a repeat earns nothing but has still used up its position

    # Best possible ordering: every relevant id first, but only k positions are available.
    ideal_hits = min(k, len(relevant_ids))
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / idcg
