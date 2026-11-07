import json
from pathlib import Path

import pytest

from driftrag.eval_cli import compare_with
from evalkit.golden import GoldenItem
from evalkit.retrieval_eval import evaluate_retrieval


def item(item_id: str) -> GoldenItem:
    return GoldenItem.model_validate(
        {
            "id": item_id,
            "lang": "en",
            "question": "A question here?",
            "category": "task",
            "relevant": [{"document": "good.md"}],
            "origin": "llm-drafted",
        }
    )


def test_paired_comparison_against_a_saved_run(tmp_path: Path) -> None:
    items = [item("aa-q1"), item("bb-q2"), item("cc-q3")]
    baseline = evaluate_retrieval(items, lambda q, lang: [("other.md", "x")], k=5)
    path = tmp_path / "baseline.json"
    path.write_text(
        json.dumps({"results": {"items": [s.__dict__ for s in baseline.items]}}), encoding="utf-8"
    )

    hits = {"aa-q1", "bb-q2"}
    order = iter(["aa-q1", "bb-q2", "cc-q3"])  # questions are evaluated in this order

    def better(question: str, lang: str) -> list[tuple[str, str]]:
        return [("good.md", "x")] if next(order) in hits else [("other.md", "x")]

    candidate = evaluate_retrieval(items, better, k=5)

    comparison = compare_with(path, candidate)
    assert comparison["n"] == 3
    assert comparison["improved"] == ["aa-q1", "bb-q2"]
    assert comparison["worse"] == []
    assert comparison["differences"]["recall_at_k"].startswith("0.667")


def test_no_common_questions_is_an_error(tmp_path: Path) -> None:
    path = tmp_path / "baseline.json"
    path.write_text(json.dumps({"results": {"items": []}}), encoding="utf-8")
    report = evaluate_retrieval([item("aa-q1")], lambda q, lang: [], k=5)
    with pytest.raises(SystemExit, match="no common questions"):
        compare_with(path, report)
