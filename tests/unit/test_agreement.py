import pytest
from hypothesis import given
from hypothesis import strategies as st

from evalkit.agreement import cohen_kappa, confusion, kappa_ci, observed_agreement


def test_textbook_example() -> None:
    # 50 items: both yes 20, A yes/B no 5, A no/B yes 10, both no 15.
    # p_o = 0.7, p_e = 0.5*0.6 + 0.5*0.4 = 0.5, kappa = 0.4.
    a = ["yes"] * 25 + ["no"] * 25
    b = ["yes"] * 20 + ["no"] * 5 + ["yes"] * 10 + ["no"] * 15
    assert observed_agreement(a, b) == pytest.approx(0.7)
    assert cohen_kappa(a, b) == pytest.approx(0.4)


def test_always_yes_judge_has_no_skill_despite_high_agreement() -> None:
    human = [True] * 9 + [False]
    judge = [True] * 10
    assert observed_agreement(human, judge) == pytest.approx(0.9)
    assert cohen_kappa(human, judge) == pytest.approx(0.0)


def test_perfect_and_opposite() -> None:
    a = [True, False, True, False]
    assert cohen_kappa(a, a) == 1.0
    assert cohen_kappa(a, [not x for x in a]) == pytest.approx(-1.0)
    assert cohen_kappa([True, True], [True, True]) == 1.0  # one label only: perfect, not NaN


def test_input_checks() -> None:
    with pytest.raises(ValueError, match="same items"):
        cohen_kappa([True], [True, False])
    with pytest.raises(ValueError, match="no items"):
        cohen_kappa([], [])


def test_interval_contains_estimate_and_is_deterministic() -> None:
    a = ["yes"] * 25 + ["no"] * 25
    b = ["yes"] * 20 + ["no"] * 5 + ["yes"] * 10 + ["no"] * 15
    first = kappa_ci(a, b, resamples=2000)
    assert first.low <= first.mean <= first.high
    assert first.mean == pytest.approx(0.4)
    assert first == kappa_ci(a, b, resamples=2000)


def test_confusion_counts() -> None:
    table = confusion(["yes", "yes", "no"], ["yes", "no", "no"])
    assert table.labels == ("no", "yes")
    assert table.counts == {("yes", "yes"): 1, ("yes", "no"): 1, ("no", "no"): 1}
    assert "yes" in str(table)


pairs = st.lists(st.tuples(st.booleans(), st.booleans()), min_size=1, max_size=60)


@given(pairs)
def test_kappa_is_bounded_and_symmetric(data: list[tuple[bool, bool]]) -> None:
    a = [x for x, _ in data]
    b = [y for _, y in data]
    kappa = cohen_kappa(a, b)
    assert -1.0 - 1e-9 <= kappa <= 1.0 + 1e-9
    assert kappa == pytest.approx(cohen_kappa(b, a))
