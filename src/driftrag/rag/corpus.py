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

from driftrag.datasets.k8s_docs import is_safe_relative


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


@dataclass(frozen=True)
class SourceDocument:
    corpus: str
    corpus_version: str
    lang: str
    path: str
    sha256: str
    text: str


def load_manifest(snapshot_dir: Path) -> SnapshotManifest:
    manifest_path = snapshot_dir / "manifest.json"
    if not manifest_path.is_file():
        raise CorpusIntegrityError(f"no manifest.json in {snapshot_dir}")
    return SnapshotManifest.model_validate_json(manifest_path.read_text(encoding="utf-8"))


def read_snapshot(snapshot_dir: Path, *, corpus: str = "k8s-docs") -> Iterator[SourceDocument]:
    """Yield every document of a snapshot, verified against the manifest, in manifest order."""
    manifest = load_manifest(snapshot_dir)
    for entry in manifest.files:
        relative = PurePosixPath(entry.path)
        if not is_safe_relative(relative):
            raise CorpusIntegrityError(f"unsafe path in manifest: {entry.path!r}")
        file_path = snapshot_dir.joinpath(*relative.parts)
        if not file_path.is_file():
            raise CorpusIntegrityError(f"missing file listed in manifest: {entry.path}")
        data = file_path.read_bytes()
        if hashlib.sha256(data).hexdigest() != entry.sha256:
            raise CorpusIntegrityError(f"checksum mismatch for {entry.path}")
        yield SourceDocument(
            corpus=corpus,
            corpus_version=manifest.version,
            lang=manifest.lang,
            path=relative.as_posix(),
            sha256=entry.sha256,
            text=data.decode("utf-8"),
        )
