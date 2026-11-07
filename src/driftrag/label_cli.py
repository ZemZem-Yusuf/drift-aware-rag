"""``driftrag-label``: rate generated answers by hand, blind to any LLM judge (experiment E4).

    uv run driftrag-label sheet --max-items 15         # writes experiments/E4-judge/LABELS.md
    (tick one box per line in LABELS.md)
    uv run driftrag-label apply --labeller "Your Name"  # adds to labels/human.jsonl

The sheet shows each answer with the question, the reference answer and the full text of the
sources the model was given, so "supported" is judged against what the model actually saw.
Completed sheets are archived in ``sheets/`` as evidence.
"""

from __future__ import annotations

import argparse
import re
import shutil
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path

from evalkit.labels import (
    AnswerLabel,
    GeneratedAnswer,
    load_answers,
    load_labels,
    save_labels,
)

REPO = Path(__file__).resolve().parents[2]
E4 = REPO / "experiments" / "E4-judge"
SHEET = E4 / "LABELS.md"
LABELS = E4 / "labels" / "human.jsonl"
ARCHIVE = E4 / "sheets"

SUPPORTED = "Supported by the sources"
CORRECT = "Correct answer to the question"
JUSTIFIED = "Refusal justified"
_FIELDS = {SUPPORTED: "supported", CORRECT: "correct", JUSTIFIED: "refusal_justified"}

_ANSWERS_MARKER = re.compile(r"^<!-- answers: (.+?) -->$", re.MULTILINE)
_BLOCK = re.compile(r"^### `([a-z0-9-]+)`", re.MULTILINE)
_LABEL_LINE = re.compile(rf"^\s*- ({SUPPORTED}|{CORRECT}|{JUSTIFIED})[^:\n]*:(.*)$", re.MULTILINE)
# Tolerant of hand-ticked boxes: "[x]", "[X]", "[x ]", "[ x]" all count.
_CHOICE = re.compile(r"\[\s*([xX]?)\s*\]\s*(yes|no)\b", re.IGNORECASE)

INSTRUCTIONS = """# Answer labelling (E4)

For each answer below, read the question, the reference answer, the system's answer and the
sources the model was given. Then tick **one box per line**:

- **Supported by the sources**: *yes* only if **every** statement in the answer is backed by
  the sources shown. Anything from outside knowledge, a wrong detail or a contradiction: *no*.
  Judge against the sources, not against what you know about Kubernetes.
- **Correct answer to the question**: *yes* if it answers the question and agrees with the
  reference answer on what matters. Wrong, missing the main point, or answering something
  else: *no*. For an out-of-scope question, an answer is never correct (it should have refused).
- **Refusal justified** (only for refusals): *yes* if the sources really don't contain the
  answer; *no* if they do and the model should have answered.

Supported and correct are separate questions: an answer can faithfully repeat the wrong sources
(supported, not correct), or be right from outside knowledge (correct, not supported).
Write anything worth remembering under **Notes** (optional).

When done, run: `uv run driftrag-label apply --labeller "Your Name"`

---
"""


def _quote(text: str) -> list[str]:
    return [f"> {line}" if line.strip() else ">" for line in text.strip().splitlines()]


def render_block(answer: GeneratedAnswer) -> str:
    lines = [
        f"### `{answer.id}`",
        "",
        f"**Question** ({answer.lang}, {answer.category}): {answer.question}",
        "",
    ]
    if answer.category == "out-of-scope":
        lines += ["**Reference answer:** *(out of scope: the system should refuse)*", ""]
    else:
        lines += [f"**Reference answer:** {answer.reference_answer}", ""]
    if answer.refused:
        lines += ["**System answer:** *refused*", "", *_quote(answer.answer), ""]
    else:
        lines += ["**System answer:**", "", *_quote(answer.answer), ""]
    if answer.invalid_citations:
        cited = ", ".join(str(n) for n in answer.invalid_citations)
        lines += [f"*Cites sources that don't exist: {cited}*", ""]
    lines += ["**Sources the model was given:**", ""]
    for source in answer.sources:
        mark = " **(cited)**" if source.cited else ""
        lines += [f"**[{source.number}]** `{source.document}`, *{source.section}*{mark}", ""]
        lines += [*_quote(source.content), ""]
    lines += ["**Labels** (tick one box per line):"]
    if answer.refused:
        lines.append(f"- {JUSTIFIED} (the answer isn't in the sources): [ ] yes [ ] no")
    else:
        lines.append(f"- {SUPPORTED}: [ ] yes [ ] no")
        lines.append(f"- {CORRECT}: [ ] yes [ ] no")
    lines += ["", "**Notes:**", "", "", "---", ""]
    return "\n".join(lines)


def to_label(answers: Sequence[GeneratedAnswer], labels: Sequence[AnswerLabel]) -> list[str]:
    """Ids still to be labelled for this answers file, in file order."""
    done = {label.id for label in labels}
    return [a.id for a in answers if a.needs_label and a.id not in done]


def render_sheet(
    answers: Sequence[GeneratedAnswer],
    answers_file: str,
    pending: Sequence[str],
    *,
    max_items: int | None = None,
) -> str:
    by_id = {a.id: a for a in answers}
    blocks = [render_block(by_id[i]) for i in list(pending)[:max_items]]
    return "\n".join([f"<!-- answers: {answers_file} -->", INSTRUCTIONS, *blocks])


@dataclass(frozen=True)
class Parsed:
    values: dict[str, bool | None] = field(default_factory=dict)
    notes: str = ""
    error: str | None = None


def answers_file_of(sheet: str) -> str | None:
    match = _ANSWERS_MARKER.search(sheet)
    return match.group(1).strip() if match else None


def parse_sheet(sheet: str) -> dict[str, Parsed]:
    parsed: dict[str, Parsed] = {}
    matches = list(_BLOCK.finditer(sheet))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(sheet)
        block = sheet[match.end() : end]
        # Only read boxes after the "Labels" heading: source text can contain anything.
        labels_part = block.split("**Labels**", 1)[1] if "**Labels**" in block else ""
        values: dict[str, bool | None] = {}
        errors: list[str] = []
        for name, rest in _LABEL_LINE.findall(labels_part.split("**Notes:**", 1)[0]):
            ticked = [choice.lower() for mark, choice in _CHOICE.findall(rest) if mark]
            if len(ticked) > 1:
                errors.append(f"both boxes ticked for '{name}'")
            values[_FIELDS[name]] = (ticked[0] == "yes") if len(ticked) == 1 else None
        notes = labels_part.split("**Notes:**", 1)[1] if "**Notes:**" in labels_part else ""
        notes = notes.replace("---", "").strip()
        parsed[match.group(1)] = Parsed(values, notes, "; ".join(errors) or None)
    return parsed


def apply_labels(
    answers: Sequence[GeneratedAnswer],
    parsed: Mapping[str, Parsed],
    existing: Sequence[AnswerLabel],
    *,
    labeller: str,
    answers_file: str,
    today: str,
) -> tuple[list[AnswerLabel], dict[str, list[str]]]:
    """Add the complete labels from a sheet. Returns all labels and a report."""
    by_id = {a.id: a for a in answers}
    labels = {(label.answers_file, label.id): label for label in existing}
    report: dict[str, list[str]] = {"labelled": [], "incomplete": [], "errors": []}
    for item_id, entry in parsed.items():
        answer = by_id.get(item_id)
        if answer is None:
            report["errors"].append(f"{item_id}: not in {answers_file}")
            continue
        if entry.error:
            report["errors"].append(f"{item_id}: {entry.error}")
            continue
        if (answers_file, item_id) in labels:
            report["errors"].append(f"{item_id}: already labelled, left unchanged")
            continue
        wanted = ("refusal_justified",) if answer.refused else ("supported", "correct")
        if any(entry.values.get(name) is None for name in wanted):
            report["incomplete"].append(item_id)
            continue
        labels[(answers_file, item_id)] = AnswerLabel(
            id=item_id,
            answers_file=answers_file,
            kind="refused" if answer.refused else "answered",
            labeller=labeller,
            labelled_at=today,
            notes=entry.notes,
            **{name: entry.values[name] for name in wanted},
        )
        report["labelled"].append(item_id)
    order = {a.id: n for n, a in enumerate(answers)}
    ordered = sorted(
        labels.values(), key=lambda label: (label.answers_file, order.get(label.id, len(order)))
    )
    return ordered, report


def latest_answers_file() -> Path:
    files = sorted((E4 / "results").glob("*-answers.json"))
    if not files:
        raise SystemExit("no answers yet: run experiments/E4-judge/generate_answers.py first")
    return files[-1]


def _archive(sheet: Path) -> Path:
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    target = ARCHIVE / f"batch-{len(list(ARCHIVE.glob('batch-*.md'))) + 1:02d}.md"
    shutil.copyfile(sheet, target)
    return target


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Label generated answers by hand (E4).")
    sub = parser.add_subparsers(dest="command", required=True)
    sheet = sub.add_parser("sheet", help=f"write {SHEET.relative_to(REPO)}")
    sheet.add_argument("--answers", type=Path, help="answers file (default: the latest)")
    sheet.add_argument("--max-items", type=int, help="only the next N answers")
    apply = sub.add_parser("apply", help="save the ticked labels")
    apply.add_argument("--labeller", required=True)
    apply.add_argument("--sheet", type=Path, default=SHEET, help="labelling sheet to read")
    args = parser.parse_args(argv)

    if args.command == "sheet":
        path = (args.answers or latest_answers_file()).resolve()
        answers_file = path.relative_to(REPO).as_posix()
        answers = load_answers(path)
        existing = [lb for lb in load_labels(LABELS) if lb.answers_file == answers_file]
        pending = to_label(answers, existing)
        SHEET.write_text(
            render_sheet(answers, answers_file, pending, max_items=args.max_items),
            encoding="utf-8",
            newline="\n",
        )
        shown = min(len(pending), args.max_items) if args.max_items else len(pending)
        print(f"wrote {SHEET.relative_to(REPO)} with {shown} of {len(pending)} answers to label")
        return

    text = args.sheet.read_text(encoding="utf-8")
    answers_file = answers_file_of(text)
    if answers_file is None:
        raise SystemExit("the sheet doesn't say which answers file it belongs to")
    answers = load_answers(REPO / answers_file)
    labels, report = apply_labels(
        answers,
        parse_sheet(text),
        load_labels(LABELS),
        labeller=args.labeller.strip(),
        answers_file=answers_file,
        today=datetime.now(UTC).date().isoformat(),
    )
    save_labels(LABELS, labels)
    if report["labelled"]:
        print(f"archived the sheet as {_archive(args.sheet).relative_to(REPO)}")
    print(f"labelled: {len(report['labelled'])}")
    for name in ("incomplete", "errors"):
        if report[name]:
            print(f"{name}:")
            for line in report[name]:
                print(f"  - {line}")
    remaining = len(to_label(answers, [lb for lb in labels if lb.answers_file == answers_file]))
    print(f"still to label: {remaining}")


if __name__ == "__main__":
    main()
