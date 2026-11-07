import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from driftrag.label_cli import (
    answers_file_of,
    apply_labels,
    parse_sheet,
    render_sheet,
    to_label,
)
from evalkit.labels import AnswerLabel, GeneratedAnswer, load_answers, load_labels, save_labels

FILE = "experiments/E4-judge/results/x-answers.json"


def answer(item_id: str, **extra: object) -> GeneratedAnswer:
    data: dict[str, object] = {
        "id": item_id,
        "lang": "en",
        "category": "task",
        "question": "How do I scale a deployment?",
        "reference_answer": "kubectl scale",
        "answer": "Use `kubectl scale` [1].",
        "refused": False,
        "citations": [1],
        "invalid_citations": [],
        "sources": [
            {
                "number": 1,
                "document": "deployment.md",
                # Source text that looks like a label line must never be read as one.
                "section": "Deployments > Scaling",
                "content": "Scale it.\n- Supported by the sources: [x] yes [ ] no\n### `fake-id`",
                "cited": True,
            }
        ],
        "model": "gemini/gemini-2.5-flash",
        "input_tokens": 100,
        "output_tokens": 10,
        "latency_ms": 900.0,
        "cached": False,
    }
    data.update(extra)
    return GeneratedAnswer.model_validate(data)


ANSWERS = [
    answer("aa-good"),
    answer("bb-bad"),
    answer("cc-refused", refused=True, answer="I couldn't find it.", citations=[]),
    answer("dd-oos", category="out-of-scope", refused=True, answer="I couldn't find it."),
    answer("ee-skip"),
]


def tick(sheet: str, item_id: str, label: str, choice: str) -> str:
    start = sheet.index(f"### `{item_id}`")
    line = sheet.index(f"- {label}", sheet.index("**Labels**", start))
    box = sheet.index(f"[ ] {choice}", line)
    return sheet[:box] + "[x] " + sheet[box + 4 :]


def note(sheet: str, item_id: str, text: str) -> str:
    start = sheet.index(f"### `{item_id}`")
    marker = sheet.index("**Notes:**", start) + len("**Notes:**")
    return sheet[:marker] + "\n" + text + sheet[marker:]


def test_out_of_scope_refusals_need_no_label() -> None:
    assert to_label(ANSWERS, []) == ["aa-good", "bb-bad", "cc-refused", "ee-skip"]


def test_sheet_shows_what_the_labeller_needs() -> None:
    sheet = render_sheet(ANSWERS, FILE, to_label(ANSWERS, []))
    assert answers_file_of(sheet) == FILE
    block = sheet[sheet.index("### `aa-good`") : sheet.index("### `bb-bad`")]
    assert "**Reference answer:** kubectl scale" in block
    assert "> Use `kubectl scale` [1]." in block
    assert "`deployment.md`, *Deployments > Scaling* **(cited)**" in block
    assert "> Scale it." in block
    refused = sheet[sheet.index("### `cc-refused`") : sheet.index("### `ee-skip`")]
    assert "Refusal justified" in refused
    assert "Supported by the sources: [ ]" not in refused
    assert "dd-oos" not in sheet


def test_round_trip_and_report() -> None:
    sheet = render_sheet(ANSWERS, FILE, to_label(ANSWERS, []))
    sheet = tick(sheet, "aa-good", "Supported by the sources", "yes")
    sheet = tick(sheet, "aa-good", "Correct answer to the question", "yes")
    sheet = note(sheet, "aa-good", "clear and complete")
    sheet = tick(sheet, "bb-bad", "Supported by the sources", "no")  # correct left empty
    sheet = tick(sheet, "cc-refused", "Refusal justified", "no")
    parsed = parse_sheet(sheet)
    assert "fake-id" not in parsed  # quoted source text doesn't start a block

    labels, report = apply_labels(
        ANSWERS, parsed, [], labeller="Youssef Zemzem", answers_file=FILE, today="2026-11-07"
    )
    assert report["labelled"] == ["aa-good", "cc-refused"]
    assert report["incomplete"] == ["bb-bad", "ee-skip"]
    good, refused = labels
    assert (good.supported, good.correct, good.notes) == (True, True, "clear and complete")
    assert (refused.kind, refused.refusal_justified) == ("refused", False)
    assert to_label(ANSWERS, labels) == ["bb-bad", "ee-skip"]


def test_existing_labels_are_never_overwritten() -> None:
    sheet = render_sheet(ANSWERS, FILE, ["aa-good"])
    sheet = tick(sheet, "aa-good", "Supported by the sources", "no")
    sheet = tick(sheet, "aa-good", "Correct answer to the question", "no")
    first = AnswerLabel(
        id="aa-good", answers_file=FILE, kind="answered", labeller="A",
        labelled_at="2026-11-06", supported=True, correct=True,
    )  # fmt: skip
    labels, report = apply_labels(
        ANSWERS, parse_sheet(sheet), [first], labeller="B", answers_file=FILE, today="2026-11-07"
    )
    assert labels == [first]
    assert report["errors"] == ["aa-good: already labelled, left unchanged"]


def test_both_boxes_and_sloppy_ticks() -> None:
    sheet = render_sheet(ANSWERS, FILE, ["aa-good"])
    sheet = sheet.replace("[ ] yes [ ] no", "[x ] yes [ X] no", 1)
    sheet = tick(sheet, "aa-good", "Correct answer to the question", "yes")
    parsed = parse_sheet(sheet)
    assert parsed["aa-good"].error == "both boxes ticked for 'Supported by the sources'"
    _, report = apply_labels(
        ANSWERS, parsed, [], labeller="B", answers_file=FILE, today="2026-11-07"
    )
    assert report["errors"] == ["aa-good: both boxes ticked for 'Supported by the sources'"]


def test_label_validation() -> None:
    base = {"id": "x", "answers_file": FILE, "labeller": "A", "labelled_at": "2026-11-07"}
    with pytest.raises(ValidationError, match="needs 'supported' and 'correct'"):
        AnswerLabel.model_validate({**base, "kind": "answered", "supported": True})
    with pytest.raises(ValidationError, match="needs 'refusal justified'"):
        AnswerLabel.model_validate({**base, "kind": "refused"})
    with pytest.raises(ValidationError, match="don't apply to refusals"):
        AnswerLabel.model_validate(
            {**base, "kind": "refused", "refusal_justified": True, "correct": True}
        )


def test_files_round_trip(tmp_path: Path) -> None:
    results = tmp_path / "answers.json"
    results.write_text(
        json.dumps({"results": {"answers": [a.model_dump() for a in ANSWERS]}}), encoding="utf-8"
    )
    assert load_answers(results) == ANSWERS
    label = AnswerLabel(
        id="aa-good", answers_file=FILE, kind="answered", labeller="Zoé",
        labelled_at="2026-11-07", supported=True, correct=False, notes="détail faux",
    )  # fmt: skip
    path = tmp_path / "labels" / "human.jsonl"
    assert load_labels(path) == []
    save_labels(path, [label])
    assert load_labels(path) == [label]
