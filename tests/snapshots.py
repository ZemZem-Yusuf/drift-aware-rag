"""Test helper: write a small corpus snapshot in the same format as the downloader."""

import hashlib
import json
from pathlib import Path


def write_snapshot(
    root: Path, files: dict[str, str], *, version: str = "1.0", lang: str = "en"
) -> Path:
    snapshot = root / f"v{version}" / lang
    entries = []
    for relative, content in files.items():
        data = content.encode("utf-8")
        target = snapshot.joinpath(*relative.split("/"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        entries.append(
            {"path": relative, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)}
        )
    manifest = {
        "source": "test",
        "ref": f"release-{version}",
        "version": version,
        "lang": lang,
        "license": "CC-BY-4.0",
        "retrieved_at": "2026-11-07T00:00:00+00:00",
        "files": entries,
    }
    (snapshot / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    return snapshot
