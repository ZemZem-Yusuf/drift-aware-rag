"""Save experiment results together with the exact setup that produced them.

A result is only worth defending if someone can answer "what produced this number?". Every
saved run therefore records, next to its results:

- **code**: git commit, and whether the working tree had uncommitted changes (a dirty run is
  flagged, not hidden);
- **software**: Python and key package versions;
- **configuration**: models and parameters (secrets are never included);
- **data**: the index version used, its embedding model, chunker config and chunk counts.

Runs are written as JSON under ``experiments/<experiment>/results/`` and committed. They are
never edited by hand; human judgements (e.g. "this answer is wrong") go in a separate,
dated annotation file next to them.
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from collections.abc import Mapping
from datetime import UTC, datetime
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import Any

from sqlalchemy import Connection, text

from driftrag.config import Settings

TRACKED_PACKAGES = (
    "drift-aware-rag",
    "litellm",
    "sentence-transformers",
    "torch",
    "sqlalchemy",
    "psycopg",
    "pgvector",
)


def git_state(repo: Path) -> dict[str, Any]:
    git = shutil.which("git")  # full path, so a look-alike earlier on PATH can't be picked up
    if git is None:
        return {"commit": None, "dirty": None}

    def run(*args: str) -> str:
        return subprocess.run(  # noqa: S603 - resolved git binary, fixed arguments
            [git, *args], cwd=repo, capture_output=True, text=True, check=True
        ).stdout.strip()

    try:
        return {"commit": run("rev-parse", "HEAD"), "dirty": bool(run("status", "--porcelain"))}
    except (OSError, subprocess.CalledProcessError):
        return {"commit": None, "dirty": None}


def package_versions(names: tuple[str, ...] = TRACKED_PACKAGES) -> dict[str, str | None]:
    versions: dict[str, str | None] = {}
    for name in names:
        try:
            versions[name] = version(name)
        except PackageNotFoundError:
            versions[name] = None
    return versions


def settings_snapshot(settings: Settings) -> dict[str, Any]:
    """Non-secret configuration that affects results. Keys and passwords are excluded."""
    return {
        "generator_model": settings.generator_model,
        "fallback_model": settings.fallback_model,
        "llm_daily_request_limits": dict(settings.llm_daily_request_limits),
        "gemini_key_configured": settings.gemini_api_key is not None,
        "groq_key_configured": settings.groq_api_key is not None,
    }


def index_snapshot(conn: Connection, version_id: int) -> dict[str, Any]:
    row = conn.execute(
        text(
            """
            SELECT v.id, v.name, v.status, v.embedding_model, v.embedding_dim,
                   v.chunker_config, v.created_at
            FROM rag.index_versions v WHERE v.id = :id
            """
        ),
        {"id": version_id},
    ).one()
    per_lang = conn.execute(
        text(
            """
            SELECT lang, count(*) AS chunks, count(DISTINCT document_id) AS documents
            FROM rag.chunks WHERE index_version_id = :id GROUP BY lang ORDER BY lang
            """
        ),
        {"id": version_id},
    ).all()
    return {
        "id": int(row.id),
        "name": str(row.name),
        "status": str(row.status),
        "embedding_model": str(row.embedding_model),
        "embedding_dim": int(row.embedding_dim),
        "chunker_config": row.chunker_config,
        "created_at": row.created_at.isoformat(),
        "per_lang": {
            str(r.lang): {"chunks": int(r.chunks), "documents": int(r.documents)} for r in per_lang
        },
    }


def environment(repo: Path, settings: Settings) -> dict[str, Any]:
    return {
        "recorded_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "git": git_state(repo),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": package_versions(),
        "settings": settings_snapshot(settings),
    }


def save_run(
    root: Path,
    experiment: str,
    name: str,
    *,
    environment: Mapping[str, Any],
    config: Mapping[str, Any],
    results: Any,
) -> Path:
    """Write one run to ``<root>/<experiment>/results/<UTC timestamp>-<name>.json``."""
    if not name.replace("-", "").replace("_", "").isalnum():
        raise ValueError("run name may contain only letters, digits, '-' and '_'")
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    path = root / experiment / "results" / f"{stamp}-{name}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "experiment": experiment,
        "run": name,
        "environment": dict(environment),
        "config": dict(config),
        "results": results,
    }
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, default=str) + "\n", encoding="utf-8"
    )
    return path
