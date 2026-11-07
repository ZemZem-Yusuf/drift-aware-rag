"""``driftrag-golden``: human review of the golden set without editing JSON by hand.

    uv run driftrag-golden sheet                         # writes golden/REVIEW.md
    (tick one box per question in REVIEW.md)
    uv run driftrag-golden apply --reviewer "Your Name"  # updates golden/k8s-1.33.jsonl

The sheet shows each draft question with its proposed answer and the actual text of the
documentation sections it points to, so the reviewer checks the item against the source, not
against memory. ``apply`` marks ticked items ``verified`` (with the reviewer's name) or
``rejected``; items needing changes stay ``draft`` and their notes are printed.
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from evalkit.golden import GoldenItem, RelevantSection, load_golden, save_golden

REPO = Path(__file__).resolve().parents[2]
GOLDEN = REPO / "golden" / "k8s-1.33.jsonl"
SHEET = REPO / "golden" / "REVIEW.md"
EXCERPT_LIMIT = 6000  # characters of documentation shown per referenced section

Decision = Literal["verified", "changes", "rejected"]
_BOXES: dict[str, Decision] = {
    "Correct as written": "verified",
    "Needs changes": "changes",
    "Reject": "rejected",
}
_BLOCK = re.compile(r"^### `([a-z0-9-]+)`", re.MULTILINE)
_BOX = re.compile(r"^- \[([ xX])\] .*?(Correct as written|Needs changes|Reject)", re.MULTILINE)

INSTRUCTIONS = """# Golden set review

For each question below:

1. Read the **question**: would a real user ask this? Is it clear and about Kubernetes v1.33?
2. Read the **documentation excerpts**: do they really answer the question? Is an obviously
   better section missing?
3. Read the **reference answer**: is it correct *according to the excerpts*?
4. Tick **exactly one** box (replace `[ ]` with `[x]`). If you pick *Needs changes*, write what
   to change under **Notes**.

Out-of-scope questions only need a check that they really are outside the Kubernetes docs.

When done, run: `uv run driftrag-golden apply --reviewer "Your Name"`

---
"""


@dataclass(frozen=True)
class Review:
    decision: Decision | None
    notes: str
    error: str | None = None


def render_sheet(
    items: Sequence[GoldenItem], excerpt: Callable[[RelevantSection, str], str | None]
) -> str:
    parts = [INSTRUCTIONS]
    for item in items:
        if item.status != "draft":
            continue
        lines = [
            f"### `{item.id}`",
            "",
            f"**Question** ({item.lang}, {item.category}): {item.question}",
            "",
        ]
        if item.category != "out-of-scope":
            lines += [f"**Reference answer:** {item.reference_answer}", ""]
            lines.append("**Relevant documentation:**")
            for section in item.relevant:
                where = section.section or "(whole document)"
                lines.append(f"- `{section.document}`, section: *{where}*")
                text = excerpt(section, item.lang)
                if text:
                    quoted = "\n".join(f"  > {line}" for line in text.splitlines() if line.strip())
                    lines.append(quoted)
            lines.append("")
        if item.notes:
            lines += [f"*Drafting note:* {item.notes}", ""]
        lines += [
            "**Decision** (tick one):",
            "- [ ] ✅ Correct as written",
            "- [ ] ✏️ Needs changes (say what under Notes)",
            "- [ ] ❌ Reject",
            "",
            "**Notes:**",
            "",
            "",
            "---",
            "",
        ]
        parts.append("\n".join(lines))
    return "\n".join(parts)


def parse_reviews(sheet: str) -> dict[str, Review]:
    reviews: dict[str, Review] = {}
    matches = list(_BLOCK.finditer(sheet))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(sheet)
        block = sheet[match.end() : end]
        ticked = [_BOXES[label] for mark, label in _BOX.findall(block) if mark.lower() == "x"]
        notes = block.split("**Notes:**", 1)[1] if "**Notes:**" in block else ""
        notes = notes.replace("---", "").strip()
        if len(ticked) > 1:
            reviews[match.group(1)] = Review(None, notes, "more than one box ticked")
        else:
            reviews[match.group(1)] = Review(ticked[0] if ticked else None, notes)
    return reviews


def apply_reviews(
    items: Sequence[GoldenItem], reviews: Mapping[str, Review], reviewer: str
) -> tuple[list[GoldenItem], dict[str, list[str]]]:
    updated: list[GoldenItem] = []
    report: dict[str, list[str]] = {
        "verified": [],
        "rejected": [],
        "changes": [],
        "unreviewed": [],
        "errors": [],
    }
    for item in items:
        review = reviews.get(item.id)
        if item.status != "draft" or review is None:
            updated.append(item)
            continue
        if review.error:
            report["errors"].append(f"{item.id}: {review.error}")
            updated.append(item)
        elif review.decision == "verified":
            updated.append(item.model_copy(update={"status": "verified", "verified_by": reviewer}))
            report["verified"].append(item.id)
        elif review.decision == "rejected":
            note = f"{item.notes} | rejected: {review.notes}".strip(" |")
            updated.append(item.model_copy(update={"status": "rejected", "notes": note}))
            report["rejected"].append(item.id)
        elif review.decision == "changes":
            report["changes"].append(f"{item.id}: {review.notes or '(no notes)'}")
            updated.append(item)
        else:
            report["unreviewed"].append(item.id)
            updated.append(item)
    return updated, report


def _db_excerpt() -> Callable[[RelevantSection, str], str | None]:
    import psycopg

    from driftrag.config import get_settings

    url = get_settings().database_url.get_secret_value()
    conn = psycopg.connect(url)

    def excerpt(section: RelevantSection, lang: str) -> str | None:
        # The whole section (all its chunks, in order), so claims can be checked against the
        # full source. Round 1 showed only the first 700 characters, which hid supporting text.
        rows = conn.execute(
            """
            SELECT c.heading_path, c.content FROM rag.chunks c
            JOIN rag.documents d ON d.id = c.document_id
            JOIN rag.index_aliases a ON a.index_version_id = c.index_version_id
            WHERE a.alias = 'active' AND d.path = %s AND c.lang = %s
              AND (%s::text IS NULL OR c.heading_path LIKE %s || '%%')
            ORDER BY c.ordinal
            """,
            (section.document, lang, section.section, section.section),
        ).fetchall()
        if not rows:
            return None
        parts: list[str] = []
        previous_heading = None
        for heading, content in rows:
            if heading != previous_heading:
                parts.append(f"[{heading}]")
                previous_heading = heading
            parts.append(str(content))
        text = "\n".join(parts)
        if len(text) > EXCERPT_LIMIT:
            text = text[:EXCERPT_LIMIT].rsplit(" ", 1)[0] + " … (section continues)"
        return text

    return excerpt


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Review the golden set.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("sheet", help=f"write {SHEET.relative_to(REPO)}")
    apply = sub.add_parser("apply", help="apply the ticked decisions")
    apply.add_argument("--reviewer", required=True)
    apply.add_argument("--sheet", type=Path, default=SHEET, help="review sheet to read")
    args = parser.parse_args(argv)

    items = load_golden(GOLDEN)
    if args.command == "sheet":
        SHEET.write_text(render_sheet(items, _db_excerpt()), encoding="utf-8", newline="\n")
        drafts = sum(i.status == "draft" for i in items)
        print(f"wrote {SHEET.relative_to(REPO)} with {drafts} questions to review")
        return

    updated, report = apply_reviews(
        items, parse_reviews(args.sheet.read_text(encoding="utf-8")), args.reviewer.strip()
    )
    save_golden(GOLDEN, updated)
    for name in ("verified", "rejected"):
        print(f"{name}: {len(report[name])}")
    for name in ("changes", "unreviewed", "errors"):
        if report[name]:
            print(f"{name}:")
            for line in report[name]:
                print(f"  - {line}")


if __name__ == "__main__":
    main()
