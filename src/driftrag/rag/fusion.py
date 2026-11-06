"""Rank fusion for hybrid retrieval.

Hybrid retrieval runs two searches over the same chunks, vector similarity (pgvector) and
keyword search (Postgres full-text), and merges the two ranked lists into one.

Their raw scores can't be added directly: cosine distance and ``ts_rank`` live on different,
non-comparable scales. Reciprocal Rank Fusion (Cormack, Clarke & Büttcher, SIGIR 2009) uses
only each document's *rank* in each list:

    score(d) = sum over lists i of  weight_i / (k + rank_i(d))

where ``rank_i(d)`` is 1-based, and a document missing from list i contributes nothing for i.
``k`` (60 in the paper) dampens the advantage of the very top ranks.
"""

from collections import defaultdict
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
    if k <= 0:
        raise ValueError(f"k must be a positive integer, got {k}")
    if weights is None:
        weights = [1.0] * len(rankings)
    if len(weights) != len(rankings):
        raise ValueError(f"weights has {len(weights)} values for {len(rankings)} rankings")
    if any(weight < 0 for weight in weights):
        raise ValueError("weights must be non-negative")

    scores: defaultdict[str, float] = defaultdict(float)
    for ranking, weight in zip(rankings, weights, strict=True):
        if len(set(ranking)) != len(ranking):
            raise ValueError("a ranking contains a duplicate id")
        for rank, doc_id in enumerate(ranking, start=1):
            scores[doc_id] += weight / (k + rank)

    # Highest score first; equal scores ordered by id so results are reproducible.
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))
