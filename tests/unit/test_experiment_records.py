import json
import shutil
import subprocess
from pathlib import Path

import pytest
from pydantic import SecretStr

from driftrag.config import Settings
from driftrag.experiments.records import environment, git_state, save_run, settings_snapshot


def test_settings_snapshot_never_contains_secrets() -> None:
    settings = Settings(
        _env_file=None,
        GEMINI_API_KEY="super-secret-key",
        database_url=SecretStr("postgresql://u:db-password@h/d"),
    )
    snapshot = json.dumps(settings_snapshot(settings))
    assert "super-secret-key" not in snapshot
    assert "db-password" not in snapshot
    assert json.loads(snapshot)["gemini_key_configured"] is True


def test_git_state_reports_commit_and_dirty_flag(tmp_path: Path) -> None:
    git_binary = shutil.which("git")
    if git_binary is None:
        pytest.skip("git is not installed")

    def git(*args: str) -> None:
        subprocess.run([git_binary, *args], cwd=tmp_path, check=True, capture_output=True)  # noqa: S603

    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (tmp_path / "a.txt").write_text("1", encoding="utf-8")
    git("add", "a.txt")
    git("commit", "-q", "-m", "init")

    clean = git_state(tmp_path)
    (tmp_path / "a.txt").write_text("2", encoding="utf-8")
    dirty = git_state(tmp_path)

    assert clean["commit"] is not None
    assert len(clean["commit"]) == 40
    assert clean["dirty"] is False
    assert dirty["dirty"] is True


def test_git_state_outside_a_repo(tmp_path: Path) -> None:
    assert git_state(tmp_path / "missing") == {"commit": None, "dirty": None}


def test_save_run_writes_a_complete_record(tmp_path: Path) -> None:
    env = environment(tmp_path, Settings(_env_file=None))
    path = save_run(
        tmp_path, "E9-test", "baseline", environment=env, config={"top_k": 5}, results=[{"x": 1}]
    )
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert path.parent == tmp_path / "E9-test" / "results"
    assert path.name.endswith("-baseline.json")
    assert saved["config"] == {"top_k": 5}
    assert saved["results"] == [{"x": 1}]
    assert {"recorded_at", "git", "python", "packages", "settings"} <= saved["environment"].keys()


@pytest.mark.parametrize("name", ["../escape", "a b", "x/y"])
def test_run_name_is_restricted(tmp_path: Path, name: str) -> None:
    with pytest.raises(ValueError, match="run name"):
        save_run(tmp_path, "E9", name, environment={}, config={}, results=[])


def test_new_result_files_do_not_make_the_tree_dirty(tmp_path: Path) -> None:
    git_binary = shutil.which("git")
    if git_binary is None:
        pytest.skip("git is not installed")

    def git(*args: str) -> None:
        subprocess.run([git_binary, *args], cwd=tmp_path, check=True, capture_output=True)  # noqa: S603

    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (tmp_path / "a.txt").write_text("1", encoding="utf-8")
    git("add", "a.txt")
    git("commit", "-q", "-m", "init")

    results = tmp_path / "experiments" / "R1" / "results"
    results.mkdir(parents=True)
    (results / "run.json").write_text("{}", encoding="utf-8")
    assert git_state(tmp_path)["dirty"] is False  # an earlier run's output

    (tmp_path / "experiments" / "R1" / "run.py").write_text("x", encoding="utf-8")
    assert git_state(tmp_path)["dirty"] is True  # an uncommitted script is real dirt
