import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from evalkit.golden import GoldenItem, RelevantSection, load_golden, save_golden, select
from evalkit.retrieval_eval import evaluate_retrieval, score_item
from evalkit.stats import bootstrap_ci, paired_difference_ci

ROLLOUT = RelevantSection(document="kubectl_rollout_restart.md")
LIMITS = RelevantSection(document="resources.md", section="Resources > Requests and limits")


def item(**overrides: object) -> GoldenItem:
    data: dict[str, object] = {
        "id": "restart-deployment",
        "lang": "en",
        "question": "How do I restart all pods of a Deployment?",
        "category": "command",
        "relevant": [ROLLOUT.model_dump()],
        "reference_answer": "kubectl rollout restart deployment/<name>",
        "origin": "llm-drafted",
    }
    data.update(overrides)
    return GoldenItem.model_validate(data)


# ---------------------------------------------------------------- golden items
def test_section_matching() -> None:
    assert ROLLOUT.matches("kubectl_rollout_restart.md", "anything")
    assert LIMITS.matches("resources.md", "Resources > Requests and limits > CPU")
    assert not LIMITS.matches("resources.md", "Resources > Quotas")
    assert not LIMITS.matches("other.md", "Resources > Requests and limits")


def test_out_of_scope_items_have_no_sources_and_others_need_one() -> None:
    item(id="capital", category="out-of-scope", relevant=[])
    with pytest.raises(ValidationError, match="must not list"):
        item(category="out-of-scope")
    with pytest.raises(ValidationError, match="at least one"):
        item(relevant=[])


def test_verified_items_name_the_reviewer() -> None:
    with pytest.raises(ValidationError, match="who verified"):
        item(status="verified")
    assert item(status="verified", verified_by="Youssef").status == "verified"


def test_load_reports_line_numbers_and_duplicates(tmp_path: Path) -> None:
    path = tmp_path / "golden.jsonl"
    save_golden(path, [item(), item(id="other")])
    assert [i.id for i in load_golden(path)] == ["restart-deployment", "other"]

    path.write_text(
        path.read_text(encoding="utf-8") + json.dumps(item().model_dump()) + "\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match=r"golden.jsonl:3: duplicate id"):
        load_golden(path)


def test_select_uses_only_verified_and_in_scope_by_default() -> None:
    items = [
        item(id="aa", status="verified", verified_by="Y"),
        item(id="bb"),  # draft
        item(id="cc", status="rejected"),
        item(id="dd", category="out-of-scope", relevant=[], status="verified", verified_by="Y"),
    ]
    assert [i.id for i in select(items)] == ["aa"]
    assert [i.id for i in select(items, include_out_of_scope=True)] == ["aa", "dd"]


# ---------------------------------------------------------------- statistics
def test_bootstrap_of_constant_values_is_exact() -> None:
    estimate = bootstrap_ci([0.5] * 20)
    assert (estimate.mean, estimate.low, estimate.high) == (0.5, 0.5, 0.5)


def test_bootstrap_interval_contains_the_mean_and_is_deterministic() -> None:
    values = [1.0] * 30 + [0.0] * 20
    first, second = bootstrap_ci(values, seed=1), bootstrap_ci(values, seed=1)
    assert first == second
    assert first.mean == pytest.approx(0.6)
    assert first.low < first.mean < first.high
    assert first.low > 0.4
    assert first.high < 0.8


def test_paired_difference() -> None:
    baseline = [0.0, 1.0, 0.0, 1.0, 0.0, 1.0]
    candidate = [1.0, 1.0, 1.0, 1.0, 0.0, 1.0]  # differences: 1, 0, 1, 0, 0, 0
    assert paired_difference_ci(baseline, candidate).mean == pytest.approx(1 / 3)
    with pytest.raises(ValueError, match="same questions"):
        paired_difference_ci([1.0], [1.0, 0.0])


def test_bootstrap_rejects_bad_input() -> None:
    with pytest.raises(ValueError, match="empty"):
        bootstrap_ci([])
    with pytest.raises(ValueError, match="confidence"):
        bootstrap_ci([1.0], confidence=1.5)


# ---------------------------------------------------------------- retrieval scoring
def test_score_item_maps_sections_and_counts_chunks_of_one_section_once() -> None:
    golden = item(relevant=[ROLLOUT.model_dump(), LIMITS.model_dump()])
    retrieved = [
        ("deployment.md", "Deployments"),
        ("kubectl_rollout_restart.md", "kubectl rollout restart"),
        ("kubectl_rollout_restart.md", "kubectl rollout restart > Options"),  # same doc again
        ("resources.md", "Resources > Requests and limits > Memory"),
    ]
    score = score_item(golden, retrieved, k=3)
    assert score.first_hit_rank == 2
    assert score.reciprocal_rank == pytest.approx(0.5)
    assert score.recall_at_k == pytest.approx(0.5)  # limits section is at rank 4 > k


def test_evaluate_retrieval_aggregates_with_intervals() -> None:
    golden = [item(id="hit"), item(id="miss")]

    def search(question: str, lang: str) -> list[tuple[str, str]]:
        return [("kubectl_rollout_restart.md", "x")] if question else []

    def search_by_id(question: str, lang: str) -> list[tuple[str, str]]:
        return search(question, lang)

    report = evaluate_retrieval(golden, search_by_id, k=5)
    assert report.recall_at_k.mean == 1.0
    assert report.recall_at_k.n == 2
    with pytest.raises(ValueError, match="verified"):
        evaluate_retrieval([], search_by_id)
