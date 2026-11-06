"""Rank fusion for hybrid retrieval.

Hybrid retrieval runs two searches over the same chunks, vector similarity (pgvector) and
keyword search (Postgres full-text), and merges the two ranked lists into one.

Their raw scores can't be added directly: cosine distance and ``ts_rank`` live on different,
non-comparable scales. Reciprocal Rank Fusion (Cormack, Clarke & Büttcher, SIGIR 2009) uses
only each document's *rank* in each list:

    score(d) = sum over lists i of  weight_i / (k + rank_i(d))

where ``rank_i(d)`` is 1-based, and a document missing from list i contributes nothing for i.
``k`` (60 in the paper) dampens the advantage of the very top ranks.

TASK (Youssef): implement ``reciprocal_rank_fusion`` so that ``tests/unit/test_fusion.py`` passes.
Write it yourself first, then ask for a review.
"""

from collections.abc import Sequence


def reciprocal_rank_fusion(
    rankings: Sequence[Sequence[str]],
    *,
    k: int = 60,
    weights: Sequence[float] | None = None,
) -> list[tuple[str, float]]:
    """Fuse several ranked lists of document ids into one ranked list.

    Args:
        rankings: one ranked list per retriever, best first. Ids are chunk ids as strings.
        k: the RRF constant. Must be > 0.
        weights: one non-negative weight per ranking. ``None`` means all weights are 1.

    Returns:
        ``(doc_id, score)`` pairs for every id that appears in any ranking, sorted by score
        (highest first). Ties are broken by doc id, ascending, so the output is deterministic.

    Raises:
        ValueError: if ``k <= 0``, if ``weights`` has a different length than ``rankings`` or
            contains a negative value, or if an id appears twice in the same ranking.
            The message must mention ``k``, ``weights`` or ``duplicate`` respectively.
    """
    raise NotImplementedError("TASK (Youssef): implement reciprocal rank fusion")
