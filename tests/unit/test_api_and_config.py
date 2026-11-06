import ast
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from driftrag import __version__
from driftrag.api.app import create_app
from driftrag.config import Settings, get_settings

SRC = Path(__file__).resolve().parents[2] / "src"


def test_health_reports_version_and_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DRIFTRAG_ENV", "test")
    get_settings.cache_clear()
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__, "env": "test"}
    get_settings.cache_clear()


def test_database_url_is_never_printed() -> None:
    settings = Settings(database_url="postgresql://user:hunter2@db/x")
    assert "hunter2" not in repr(settings)
    assert "hunter2" not in str(settings.model_dump())


def test_evalkit_does_not_import_driftrag() -> None:
    """evalkit is shared with other projects, so it must stay independent of driftrag."""
    import evalkit

    assert evalkit.__doc__
    offenders = []
    for path in (SRC / "evalkit").rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            offenders += [f"{path.name}: {n}" for n in names if n.split(".")[0] == "driftrag"]
    assert offenders == []
