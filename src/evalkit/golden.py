"""Golden set: questions with known relevant sources and a reference answer.

Stored as JSON Lines (one item per line) so diffs are readable in review.

Relevance is recorded per **document + section**, never per chunk id. Chunk ids change every
time the corpus is re-chunked or re-indexed, and a golden set that breaks on re-indexing is
useless for a system whose job is to re-index safely. A retrieved chunk counts as relevant if
its document matches and its section path starts with the recorded section (``section=None``
means any part of the document is relevant).

Every item carries a review status. Only ``verified`` items are used for reported numbers;
drafts are excluded so unchecked questions never inflate or deflate a result.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Category = Literal["concept", "task", "command", "troubleshooting", "out-of-scope"]
Status = Literal["draft", "verified", "rejected"]


class RelevantSection(BaseModel):
    model_config = ConfigDict(frozen=True)

    document: str = Field(min_length=1)
    section: str | None = None

    def matches(self, document: str, heading_path: str) -> bool:
        if document != self.document:
            return False
        return self.section is None or heading_path.startswith(self.section)

    @property
    def key(self) -> str:
        return f"{self.document}::{self.section or '*'}"


class GoldenItem(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str = Field(pattern=r"^[a-z0-9][a-z0-9-]{1,63}$")
    lang: Literal["en", "fr"]
    question: str = Field(min_length=5)
    category: Category
    relevant: tuple[RelevantSection, ...] = ()
    reference_answer: str = ""
    status: Status = "draft"
    origin: Literal["hand-written", "llm-drafted"]
    verified_by: str | None = None
    notes: str = ""

    @model_validator(mode="after")
    def _consistent(self) -> GoldenItem:
        if self.category == "out-of-scope":
            if self.relevant:
                raise ValueError(f"{self.id}: out-of-scope items must not list relevant sources")
        elif not self.relevant:
            raise ValueError(f"{self.id}: at least one relevant source is required")
        if self.status == "verified" and not self.verified_by:
            raise ValueError(f"{self.id}: verified items must say who verified them")
        return self

    def relevant_keys_for(self, document: str, heading_path: str) -> list[str]:
        return [r.key for r in self.relevant if r.matches(document, heading_path)]


def load_golden(path: Path) -> list[GoldenItem]:
    items: list[GoldenItem] = []
    seen: set[str] = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            item = GoldenItem.model_validate(json.loads(line))
        except (json.JSONDecodeError, ValueError) as exc:
            raise ValueError(f"{path.name}:{number}: {exc}") from exc
        if item.id in seen:
            raise ValueError(f"{path.name}:{number}: duplicate id '{item.id}'")
        seen.add(item.id)
        items.append(item)
    return items


def save_golden(path: Path, items: Iterable[GoldenItem]) -> None:
    lines = [json.dumps(i.model_dump(exclude_defaults=False), ensure_ascii=False) for i in items]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def select(
    items: Sequence[GoldenItem],
    *,
    statuses: Sequence[Status] = ("verified",),
    include_out_of_scope: bool = False,
) -> list[GoldenItem]:
    return [
        i
        for i in items
        if i.status in statuses and (include_out_of_scope or i.category != "out-of-scope")
    ]
