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

TASK (Youssef): implement the three functions so that ``tests/unit/test_metrics.py`` passes.
Write them yourself first, then ask for a review. Be ready to explain in an interview when
you'd pick each metric.
"""

from collections.abc import Collection, Sequence


def recall_at_k(retrieved: Sequence[str], relevant: Collection[str], k: int) -> float:
    """Share of relevant ids found in the first ``k`` retrieved ids.

    Raises:
        ValueError: if ``k <= 0`` or ``relevant`` is empty (recall is undefined).
    """
    raise NotImplementedError("TASK (Youssef)")


def reciprocal_rank(retrieved: Sequence[str], relevant: Collection[str]) -> float:
    """``1 / rank`` of the first relevant id (rank is 1-based), or ``0.0`` if none is retrieved.

    Raises:
        ValueError: if ``relevant`` is empty.
    """
    raise NotImplementedError("TASK (Youssef)")


def ndcg_at_k(retrieved: Sequence[str], relevant: Collection[str], k: int) -> float:
    """Normalised discounted cumulative gain at ``k``, with binary relevance.

    ``DCG  = sum over the first k positions i (1-based) of rel_i / log2(i + 1)``
    ``IDCG = sum for i = 1 .. min(k, len(relevant)) of 1 / log2(i + 1)``
    ``nDCG = DCG / IDCG``

    Raises:
        ValueError: if ``k <= 0`` or ``relevant`` is empty.
    """
    raise NotImplementedError("TASK (Youssef)")
