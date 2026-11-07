"""Generated answers and the human labels attached to them (experiment E4).

A ``GeneratedAnswer`` is everything a labeller (or a judge) needs to rate one answer: the
question, the reference answer, the system's answer and the exact sources the model saw. An
``AnswerLabel`` is one person's rating of one answer. Labels are human judgements, so they are
stored apart from the generated results (``labels/*.jsonl``) and never edited by scripts that
generate data.
"""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from evalkit.golden import Category


class Source(BaseModel):
    model_config = ConfigDict(frozen=True)

    number: int = Field(ge=1)
    document: str
    section: str
    content: str
    cited: bool


class GeneratedAnswer(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    lang: Literal["en", "fr"]
    category: Category
    question: str
    reference_answer: str
    answer: str
    refused: bool
    citations: list[int]
    invalid_citations: list[int]
    sources: list[Source]
    model: str | None
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cached: bool

    @property
    def needs_label(self) -> bool:
        """A refused out-of-scope question is correct by definition; everything else is rated."""
        return not (self.refused and self.category == "out-of-scope")


def load_answers(path: Path) -> list[GeneratedAnswer]:
    """Answers from a results file written by ``experiments/E4-judge/generate_answers.py``."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [GeneratedAnswer.model_validate(a) for a in payload["results"]["answers"]]


class AnswerLabel(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    answers_file: str
    kind: Literal["answered", "refused"]
    labeller: str = Field(min_length=1)
    labelled_at: str
    supported: bool | None = None
    correct: bool | None = None
    refusal_justified: bool | None = None
    notes: str = ""

    @model_validator(mode="after")
    def _complete(self) -> AnswerLabel:
        if self.kind == "answered":
            if self.supported is None or self.correct is None:
                raise ValueError(f"{self.id}: an answered item needs 'supported' and 'correct'")
            if self.refusal_justified is not None:
                raise ValueError(f"{self.id}: 'refusal justified' only applies to refusals")
        else:
            if self.refusal_justified is None:
                raise ValueError(f"{self.id}: a refusal needs 'refusal justified'")
            if self.supported is not None or self.correct is not None:
                raise ValueError(f"{self.id}: 'supported' and 'correct' don't apply to refusals")
        return self


def load_labels(path: Path) -> list[AnswerLabel]:
    if not path.exists():
        return []
    return [
        AnswerLabel.model_validate_json(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def save_labels(path: Path, labels: Iterable[AnswerLabel]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(label.model_dump(), ensure_ascii=False) for label in labels]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
