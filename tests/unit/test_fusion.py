"""Spec for reciprocal_rank_fusion. Implement src/driftrag/rag/fusion.py until these pass."""

import pytest
from hypothesis import given
from hypothesis import strategies as st

from driftrag.rag.fusion import reciprocal_rank_fusion


def ids(result: list[tuple[str, float]]) -> list[str]:
    return [doc for doc, _ in result]


def test_single_ranking_keeps_its_order_with_rrf_scores() -> None:
    result = reciprocal_rank_fusion([["a", "b"]])
    assert ids(result) == ["a", "b"]
    assert result[0][1] == pytest.approx(1 / 61)
    assert result[1][1] == pytest.approx(1 / 62)


def test_two_rankings_are_fused() -> None:
    vector = ["a", "b", "c"]
    keyword = ["c", "a", "d"]
    result = dict(reciprocal_rank_fusion([vector, keyword]))
    assert result["a"] == pytest.approx(1 / 61 + 1 / 62)
    assert result["c"] == pytest.approx(1 / 63 + 1 / 61)
    assert result["b"] == pytest.approx(1 / 62)
    assert result["d"] == pytest.approx(1 / 63)
    assert ids(reciprocal_rank_fusion([vector, keyword])) == ["a", "c", "b", "d"]


def test_weights_change_the_order() -> None:
    result = reciprocal_rank_fusion([["a", "b", "c"], ["c", "a", "d"]], weights=[1, 3])
    assert ids(result) == ["c", "a", "d", "b"]
    assert dict(result)["d"] == pytest.approx(3 / 63)


def test_custom_k() -> None:
    ((doc, score),) = reciprocal_rank_fusion([["a"]], k=1)
    assert doc == "a"
    assert score == pytest.approx(0.5)


def test_ties_are_broken_by_id() -> None:
    assert ids(reciprocal_rank_fusion([["b"], ["a"]])) == ["a", "b"]
    assert ids(reciprocal_rank_fusion([["a"], ["b"]])) == ["a", "b"]


def test_empty_inputs() -> None:
    assert reciprocal_rank_fusion([]) == []
    assert reciprocal_rank_fusion([[], []]) == []


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"rankings": [["a"]], "k": 0}, "k"),
        ({"rankings": [["a"]], "weights": [1, 1]}, "weights"),
        ({"rankings": [["a"]], "weights": [-1]}, "weights"),
        ({"rankings": [["a", "a"]]}, "duplicate"),
    ],
)
def test_invalid_input_is_rejected(kwargs: dict[str, object], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        reciprocal_rank_fusion(**kwargs)  # type: ignore[arg-type]


rankings_strategy = st.lists(
    st.lists(st.sampled_from("abcdefgh"), unique=True, max_size=8), max_size=4
)


@given(rankings_strategy)
def test_output_is_the_union_sorted_by_score(rankings: list[list[str]]) -> None:
    result = reciprocal_rank_fusion(rankings)
    assert sorted(ids(result)) == sorted({doc for ranking in rankings for doc in ranking})
    scores = [score for _, score in result]
    assert scores == sorted(scores, reverse=True)
    assert all(score > 0 for score in scores)
