"""Read a downloaded corpus snapshot and verify it against its manifest.

A snapshot folder (written by ``driftrag.datasets.k8s_docs``) contains Markdown files and a
``manifest.json`` with the SHA-256 of every file. Ingestion only accepts files whose content
matches the manifest, so anything modified after download, by accident or by an attacker, is
refused before it reaches the index (threat model T1: provenance).
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from pydantic import BaseModel

from driftrag.datasets.k8s_docs import EXAMPLES_DIR, is_safe_relative
from driftrag.rag.code_samples import resolve_code_samples


class CorpusIntegrityError(RuntimeError):
    """A file is missing, unsafe, or doesn't match its recorded checksum."""


class ManifestFile(BaseModel):
    path: str
    sha256: str
    bytes: int


class SnapshotManifest(BaseModel):
    source: str
    ref: str
    version: str
    lang: str
    license: str
    retrieved_at: str
    files: list[ManifestFile]
    examples: list[ManifestFile] = []  # absent in snapshots downloaded before examples existed


@dataclass(frozen=True)
class SourceDocument:
    corpus: str
    corpus_version: str
    lang: str
    path: str
    sha256: str  # of the page file as downloaded (provenance), before any sample is inlined
    text: str


@dataclass
class SampleStats:
    resolved: int = 0
    missing: int = 0


def load_manifest(snapshot_dir: Path) -> SnapshotManifest:
    manifest_path = snapshot_dir / "manifest.json"
    if not manifest_path.is_file():
        raise CorpusIntegrityError(f"no manifest.json in {snapshot_dir}")
    return SnapshotManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))


def _verified_bytes(root: Path, entry: ManifestFile) -> bytes:
    relative = PurePosixPath(entry.path)
    if not is_safe_relative(relative):
        raise CorpusIntegrityError(f"unsafe path in manifest: {entry.path!r}")
    file_path = root.joinpath(*relative.parts)
    if not file_path.is_file():
        raise CorpusIntegrityError(f"missing file listed in manifest: {entry.path}")
    data = file_path.read_bytes()
    if hashlib.sha256(data).hexdigest() != entry.sha256:
        raise CorpusIntegrityError(f"checksum mismatch for {entry.path}")
    return data


def load_examples(snapshot_dir: Path) -> dict[str, str]:
    """All example files of a snapshot, checksum-verified, keyed by path below examples/."""
    manifest = load_manifest(snapshot_dir)
    root = snapshot_dir / EXAMPLES_DIR
    return {
        PurePosixPath(e.path).as_posix(): _verified_bytes(root, e).decode("utf-8")
        for e in manifest.examples
    }


def read_snapshot(
    snapshot_dir: Path,
    *,
    corpus: str = "k8s-docs",
    code_samples: bool = False,
    stats: SampleStats | None = None,
) -> Iterator[SourceDocument]:
    """Yield every document of a snapshot, verified against the manifest, in manifest order.

    With ``code_samples=True``, example files included through shortcodes are inlined into the
    page text. Like the website, a translated page falls back to the English examples
    (the sibling ``en`` snapshot) when its own language has no such file.
    """
    manifest = load_manifest(snapshot_dir)
    lookup = None
    if code_samples:
        examples = load_examples(snapshot_dir)
        english = snapshot_dir.parent / "en"
        fallback = (
            load_examples(english)
            if manifest.lang != "en" and (english / "manifest.json").is_file()
            else {}
        )

        def lookup(path: str) -> str | None:
            return examples.get(path) or fallback.get(path)

    for entry in manifest.files:
        text = _verified_bytes(snapshot_dir, entry).decode("utf-8")
        if lookup is not None:
            resolution = resolve_code_samples(text, lookup)
            text = resolution.text
            if stats is not None:
                stats.resolved += resolution.resolved
                stats.missing += len(resolution.missing)
        yield SourceDocument(
            corpus=corpus,
            corpus_version=manifest.version,
            lang=manifest.lang,
            path=PurePosixPath(entry.path).as_posix(),
            sha256=entry.sha256,
            text=text,
        )
