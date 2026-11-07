"""Test helper: write a small corpus snapshot in the same format as the downloader."""

import hashlib
import json
from pathlib import Path


def _write_files(base: Path, files: dict[str, str]) -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    for relative, content in files.items():
        data = content.encode("utf-8")
        target = base.joinpath(*relative.split("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        entries.append(
            {"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        )
    return entries


def write_snapshot(
    root: Path,
    files: dict[str, str],
    *,
    version: str = "1.0",
    lang: str = "en",
    examples: dict[str, str] | None = None,
) -> Path:
    snapshot = root / f"v{version}" / lang
    manifest = {
        "source": "test",
        "ref": f"release-{version}",
        "version": version,
        "lang": lang,
        "license": "CC-BY-4.0",
        "retrieved_at": "2026-11-07T00:00:00+00:00",
        "files": _write_files(snapshot, files),
        "examples": _write_files(snapshot / "_examples", examples or {}),
    }
    (snapshot / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return snapshot
