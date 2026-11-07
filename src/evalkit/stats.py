"""Confidence intervals for metrics averaged over a small question set.

With ~50 questions, a mean recall of 0.80 could easily be 0.70 or 0.88 on another sample of
questions. Reporting a number without its interval invites conclusions the data can't support
("the reranker improved recall by 2 points"). The percentile bootstrap resamples the questions
with replacement many times and reads the interval from the spread of the resampled means.

Paired comparison: to compare two systems on the *same* questions, resample the per-question
*differences*. That's much tighter than comparing two separate intervals, because question
difficulty cancels out.
"""

from __future__ import annotations

import random
from collections.abc import Sequence
from dataclasses import dataclass


@dataclass(frozen=True)
class Estimate:
    mean: float
    low: float
    high: float
    n: int

    def __str__(self) -> str:
        return f"{self.mean:.3f} [{self.low:.3f}, {self.high:.3f}] (n={self.n})"


def bootstrap_ci(
    values: Sequence[float],
    *,
    confidence: float = 0.95,
    resamples: int = 10_000,
    seed: int = 0,
) -> Estimate:
    """Mean and percentile-bootstrap interval. Deterministic for a given seed."""
    if not values:
        raise ValueError("values must not be empty")
    if not 0 < confidence < 1:
        raise ValueError("confidence must be between 0 and 1")
    n = len(values)
    mean = sum(values) / n
    rng = random.Random(seed)  # noqa: S311 - statistical resampling, not security
    means = sorted(sum(rng.choices(values, k=n)) / n for _ in range(resamples))
    alpha = (1 - confidence) / 2
    low = means[int(alpha * (resamples - 1))]
    high = means[int((1 - alpha) * (resamples - 1))]
    return Estimate(mean=mean, low=low, high=high, n=n)


def paired_difference_ci(
    baseline: Sequence[float],
    candidate: Sequence[float],
    *,
    confidence: float = 0.95,
    resamples: int = 10_000,
    seed: int = 0,
) -> Estimate:
    """Interval for mean(candidate - baseline) over the same questions, in the same order."""
    if len(baseline) != len(candidate):
        raise ValueError("baseline and candidate must score the same questions")
    differences = [c - b for b, c in zip(baseline, candidate, strict=True)]
    return bootstrap_ci(differences, confidence=confidence, resamples=resamples, seed=seed)
