"""Agreement between two raters labelling the same items (e.g. a human and an LLM judge).

Raw agreement overstates how good a judge is when one label dominates: if 90% of answers are
"supported", a judge that always says "supported" agrees 90% of the time and knows nothing.
Cohen's κ corrects for that:

    κ = (p_o - p_e) / (1 - p_e)

where p_o is the observed agreement and p_e the agreement expected by chance from each
rater's own label frequencies. κ = 1 is perfect agreement, 0 is chance level, < 0 is worse than
chance. The interval comes from resampling the items (percentile bootstrap), as for the
retrieval metrics.
"""

from __future__ import annotations

import random
from collections import Counter
from collections.abc import Hashable, Sequence
from dataclasses import dataclass

from evalkit.stats import Estimate


def _check(a: Sequence[Hashable], b: Sequence[Hashable]) -> None:
    if len(a) != len(b):
        raise ValueError("both raters must label the same items, in the same order")
    if not a:
        raise ValueError("no items to compare")


def observed_agreement(a: Sequence[Hashable], b: Sequence[Hashable]) -> float:
    _check(a, b)
    return sum(x == y for x, y in zip(a, b, strict=True)) / len(a)


def cohen_kappa(a: Sequence[Hashable], b: Sequence[Hashable]) -> float:
    """Cohen's κ for two raters. Perfect agreement gives 1.0 (also when only one label is used)."""
    p_o = observed_agreement(a, b)
    if p_o == 1.0:
        return 1.0  # includes the degenerate case where both raters use a single label
    n = len(a)
    count_a, count_b = Counter(a), Counter(b)
    p_e = sum(count_a[label] * count_b[label] for label in count_a) / (n * n)
    return (p_o - p_e) / (1 - p_e)  # p_e < 1 here, since p_e == 1 implies p_o == 1


def kappa_ci(
    a: Sequence[Hashable],
    b: Sequence[Hashable],
    *,
    confidence: float = 0.95,
    resamples: int = 10_000,
    seed: int = 0,
) -> Estimate:
    """κ with a percentile-bootstrap interval over items. Deterministic for a given seed."""
    _check(a, b)
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    pairs = list(zip(a, b, strict=True))
    n = len(pairs)
    rng = random.Random(seed)  # noqa: S311 - statistical resampling, not security
    kappas = []
    for _ in range(resamples):
        sample = rng.choices(pairs, k=n)
        kappas.append(cohen_kappa([x for x, _ in sample], [y for _, y in sample]))
    kappas.sort()
    alpha = (1 - confidence) / 2
    return Estimate(
        mean=cohen_kappa(a, b),
        low=kappas[int(alpha * (resamples - 1))],
        high=kappas[int((1 - alpha) * (resamples - 1))],
        n=n,
    )


@dataclass(frozen=True)
class Confusion:
    """Counts of (rater A label, rater B label) pairs, e.g. (human, judge)."""

    labels: tuple[Hashable, ...]
    counts: dict[tuple[Hashable, Hashable], int]

    def __str__(self) -> str:
        width = max(len(str(label)) for label in self.labels) + 2
        header = " " * width + "".join(f"{label!s:>{width}}" for label in self.labels)
        rows = [
            f"{row!s:<{width}}"
            + "".join(f"{self.counts.get((row, col), 0):>{width}}" for col in self.labels)
            for row in self.labels
        ]
        return "\n".join([header, *rows])


def confusion(a: Sequence[Hashable], b: Sequence[Hashable]) -> Confusion:
    _check(a, b)
    labels = tuple(sorted({*a, *b}, key=str))
    return Confusion(labels, dict(Counter(zip(a, b, strict=True))))
