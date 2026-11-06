"""Spec for evalkit.metrics. Implement src/evalkit/metrics.py until these pass."""

import math

import pytest
from hypothesis import given
from hypothesis import strategies as st

from evalkit.metrics import ndcg_at_k, recall_at_k, reciprocal_rank

RETRIEVED = ["a", "b", "c", "d"]


# ---------------------------------------------------------------- recall@k
@pytest.mark.parametrize(("k", "expected"), [(1, 0.0), (2, 1 / 3), (4, 2 / 3), (10, 2 / 3)])
def test_recall_at_k(k: int, expected: float) -> None:
    assert recall_at_k(RETRIEVED, {"b", "d", "x"}, k) == pytest.approx(expected)


def test_recall_counts_duplicates_once() -> None:
    assert recall_at_k(["b", "b", "c"], {"b", "c"}, k=2) == pytest.approx(0.5)


def test_recall_with_nothing_retrieved() -> None:
    assert recall_at_k([], {"a"}, k=5) == 0.0


# ---------------------------------------------------------------- reciprocal rank
@pytest.mark.parametrize(
    ("relevant", "expected"),
    [({"c"}, 1 / 3), ({"a", "c"}, 1.0), ({"z"}, 0.0), ({"d", "c"}, 1 / 3)],
)
def test_reciprocal_rank(relevant: set[str], expected: float) -> None:
    assert reciprocal_rank(RETRIEVED, relevant) == pytest.approx(expected)


def test_duplicates_keep_their_slot_in_reciprocal_rank() -> None:
    # The second "a" wastes position 2; "b" is still at rank 3, not moved up to 2.
    assert reciprocal_rank(["a", "a", "b"], {"b"}) == pytest.approx(1 / 3)


# ---------------------------------------------------------------- nDCG@k
def test_ndcg_known_value() -> None:
    dcg = 1 / math.log2(3) + 1 / math.log2(4)
    idcg = 1 + 1 / math.log2(3)
    assert ndcg_at_k(["a", "b", "c"], {"b", "c"}, k=3) == pytest.approx(dcg / idcg)


def test_ndcg_perfect_and_zero() -> None:
    assert ndcg_at_k(["b", "c", "a"], {"b", "c"}, k=3) == pytest.approx(1.0)
    assert ndcg_at_k(["a", "b"], {"b"}, k=1) == 0.0


def test_ndcg_ideal_is_limited_by_k() -> None:
    # 3 relevant docs but k=1: the best possible is one hit at rank 1, so a hit there is perfect.
    assert ndcg_at_k(["a", "x"], {"a", "b", "c"}, k=1) == pytest.approx(1.0)


def test_ndcg_counts_duplicates_once() -> None:
    expected = (1 + 1 / math.log2(4)) / (1 + 1 / math.log2(3))
    assert ndcg_at_k(["b", "b", "c"], {"b", "c"}, k=3) == pytest.approx(expected)


# ---------------------------------------------------------------- invalid input
@pytest.mark.parametrize("k", [0, -1])
def test_k_must_be_positive(k: int) -> None:
    with pytest.raises(ValueError, match="k"):
        recall_at_k(RETRIEVED, {"a"}, k)
    with pytest.raises(ValueError, match="k"):
        ndcg_at_k(RETRIEVED, {"a"}, k)


def test_empty_relevant_set_is_rejected() -> None:
    with pytest.raises(ValueError, match="relevant"):
        recall_at_k(RETRIEVED, set(), 3)
    with pytest.raises(ValueError, match="relevant"):
        reciprocal_rank(RETRIEVED, set())
    with pytest.raises(ValueError, match="relevant"):
        ndcg_at_k(RETRIEVED, set(), 3)


# ---------------------------------------------------------------- properties
docs = st.lists(st.sampled_from("abcdefgh"), max_size=10)
relevant_sets = st.sets(st.sampled_from("abcdefgh"), min_size=1)


@given(docs, relevant_sets, st.integers(min_value=1, max_value=10))
def test_metrics_stay_between_zero_and_one(
    retrieved: list[str], relevant: set[str], k: int
) -> None:
    for value in (
        recall_at_k(retrieved, relevant, k),
        reciprocal_rank(retrieved, relevant),
        ndcg_at_k(retrieved, relevant, k),
    ):
        assert 0.0 <= value <= 1.0 + 1e-12


@given(docs, relevant_sets, st.integers(min_value=1, max_value=9))
def test_recall_never_decreases_with_k(retrieved: list[str], relevant: set[str], k: int) -> None:
    assert recall_at_k(retrieved, relevant, k) <= recall_at_k(retrieved, relevant, k + 1)
