"""Markdown chunking for Hugo documentation pages (the Kubernetes docs).

Pipeline for one page:

1. Split off the YAML front matter and read the page title.
2. Clean Hugo-specific markup: ``{{< glossary_tooltip text="X" ... >}}`` becomes ``X`` (it sits
   inside sentences), other shortcodes and HTML comments are dropped, and links keep only their
   text (URLs are noise for embeddings).
3. Split into sections at Markdown headings, ignoring ``#`` lines inside code blocks, and keep
   each section's heading path ("Pods > Using Pods > Workload resources").
4. Pack paragraphs into chunks of at most ``max_chars``, with a small paragraph overlap between
   consecutive chunks of the same section. Oversized paragraphs are split on line breaks, then
   hard-cut as a last resort.

The configuration is versioned: ``ChunkerConfig.config_id`` is a hash of every parameter and is
stored with the index version, so any retrieval result can be traced to the chunking that
produced it.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

_FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_TITLE = re.compile(r"^title:\s*(.+?)\s*$", re.MULTILINE)
_TOOLTIP = re.compile(r"\{\{[<%]\s*glossary_tooltip\b[^}]*?\btext=\"([^\"]*)\"[^}]*?[>%]\}\}")
_SHORTCODE = re.compile(r"\{\{[<%].*?[>%]\}\}", re.DOTALL)
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_IMAGE = re.compile(r"!\[([^\]]*)\]\([^)]*\)")
_LINK = re.compile(r"\[([^\]]+)\]\([^)]*\)")
_HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^\s*(```|~~~)")
_BLANK_RUNS = re.compile(r"\n{3,}")


class ChunkerConfig(BaseModel):
    """All chunking parameters. Changing any of them changes ``config_id``."""

    model_config = ConfigDict(frozen=True)

    strategy: Literal["markdown-headings"] = "markdown-headings"
    version: int = 1
    max_chars: int = Field(default=1200, ge=200)
    overlap_chars: int = Field(default=200, ge=0)
    min_chars: int = Field(default=80, ge=0)

    @model_validator(mode="after")
    def _overlap_smaller_than_chunk(self) -> ChunkerConfig:
        if self.overlap_chars >= self.max_chars // 2:
            raise ValueError("overlap_chars must be less than half of max_chars")
        return self

    @property
    def config_id(self) -> str:
        payload = json.dumps(self.model_dump(), sort_keys=True).encode()
        return hashlib.sha256(payload).hexdigest()[:12]


@dataclass(frozen=True)
class Chunk:
    ordinal: int
    heading_path: str
    content: str


@dataclass(frozen=True)
class Page:
    title: str
    body: str


def parse_page(markdown: str, *, fallback_title: str = "") -> Page:
    """Split front matter from the body and return the title and the cleaned body."""
    title = fallback_title
    body = markdown
    match = _FRONT_MATTER.match(markdown)
    if match:
        body = markdown[match.end() :]
        title_match = _TITLE.search(match.group(1))
        if title_match:
            title = title_match.group(1).strip().strip("\"'")
    return Page(title=title, body=clean_markup(body))


def clean_markup(text: str) -> str:
    """Remove Hugo markup that carries no meaning for retrieval. Code blocks are kept as is."""
    text = _TOOLTIP.sub(r"\1", text)
    text = _SHORTCODE.sub("", text)
    text = _COMMENT.sub("", text)
    text = _IMAGE.sub(r"\1", text)
    text = _LINK.sub(r"\1", text)
    text = "\n".join(line.rstrip() for line in text.splitlines())
    return _BLANK_RUNS.sub("\n\n", text).strip()


def split_sections(title: str, body: str) -> list[tuple[str, str]]:
    """Split a cleaned body at headings. Returns ``(heading_path, text)`` pairs, in order."""
    sections: list[tuple[str, str]] = []
    stack: list[tuple[int, str]] = []  # (level, heading) of the current section's ancestors
    lines: list[str] = []
    in_code = False

    def path() -> str:
        parts = ([title] if title else []) + [heading for _, heading in stack]
        return " > ".join(parts)

    def flush() -> None:
        text = "\n".join(lines).strip()
        if text:
            sections.append((path(), text))
        lines.clear()

    for line in body.splitlines():
        if _FENCE.match(line):
            in_code = not in_code
        heading = None if in_code else _HEADING.match(line)
        if heading:
            flush()
            level = len(heading.group(1))
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, heading.group(2).strip()))
        else:
            lines.append(line)
    flush()
    return sections


def _paragraphs(text: str) -> list[str]:
    """Split on blank lines, keeping fenced code blocks whole even if they contain blank lines."""
    paragraphs: list[str] = []
    current: list[str] = []
    in_code = False
    for line in text.splitlines():
        if _FENCE.match(line):
            in_code = not in_code
        if not line.strip() and not in_code:
            if current:
                paragraphs.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        paragraphs.append("\n".join(current))
    return paragraphs


def _fit(paragraph: str, max_chars: int) -> list[str]:
    """Break one paragraph into pieces of at most ``max_chars``: on lines first, then hard cuts."""
    if len(paragraph) <= max_chars:
        return [paragraph]
    pieces: list[str] = []
    current = ""
    for line in paragraph.splitlines():
        while len(line) > max_chars:
            if current:
                pieces.append(current)
                current = ""
            pieces.append(line[:max_chars])
            line = line[max_chars:]
        candidate = f"{current}\n{line}" if current else line
        if len(candidate) <= max_chars:
            current = candidate
        else:
            pieces.append(current)
            current = line
    if current:
        pieces.append(current)
    return pieces


def _pack(text: str, config: ChunkerConfig) -> list[str]:
    """Greedily pack paragraphs into chunks, starting each new chunk with a short overlap."""
    pieces = [p for paragraph in _paragraphs(text) for p in _fit(paragraph, config.max_chars)]
    chunks: list[str] = []
    current: list[str] = []

    def size(parts: list[str]) -> int:
        return sum(len(p) for p in parts) + 2 * max(len(parts) - 1, 0)

    for piece in pieces:
        if current and size([*current, piece]) > config.max_chars:
            chunks.append("\n\n".join(current))
            overlap = current[-1]
            fits = len(overlap) <= config.overlap_chars
            current = [overlap] if fits and size([overlap, piece]) <= config.max_chars else []
        current.append(piece)
    if current:
        chunks.append("\n\n".join(current))
    return chunks


def chunk_page(markdown: str, config: ChunkerConfig, *, fallback_title: str = "") -> list[Chunk]:
    """Turn one Markdown page into ordered chunks. Deterministic for a given config."""
    page = parse_page(markdown, fallback_title=fallback_title)
    chunks: list[Chunk] = []
    for heading_path, text in split_sections(page.title, page.body):
        for content in _pack(text, config):
            previous = chunks[-1] if chunks else None
            too_small = len(content) < config.min_chars
            if too_small and previous is not None and previous.heading_path == heading_path:
                merged = f"{previous.content}\n\n{content}"
                if len(merged) <= config.max_chars:
                    chunks[-1] = Chunk(previous.ordinal, heading_path, merged)
                    continue
            chunks.append(Chunk(ordinal=len(chunks), heading_path=heading_path, content=content))
    return chunks
