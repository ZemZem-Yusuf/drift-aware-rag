import gzip
import io
import json
import tarfile
from pathlib import Path, PurePosixPath

import pytest

from driftrag.datasets.k8s_docs import (
    docs_relative_path,
    download,
    extract_docs,
    is_safe_relative,
    main,
)

TOP = "website-release-1.33"


def make_archive(files: dict[str, bytes]) -> io.BytesIO:
    raw = io.BytesIO()
    with tarfile.open(fileobj=raw, mode="w") as tar:
        for name, data in files.items():
            info = tarfile.TarInfo(name)
            info.size = len(data)
            tar.addfile(info, io.BytesIO(data))
    return io.BytesIO(gzip.compress(raw.getvalue()))


@pytest.mark.parametrize(
    ("name", "lang", "expected"),
    [
        (f"{TOP}/content/en/docs/concepts/pods.md", "en", "concepts/pods.md"),
        (f"{TOP}/content/fr/docs/concepts/pods.md", "fr", "concepts/pods.md"),
        (f"{TOP}/content/fr/docs/concepts/pods.md", "en", None),
        (f"{TOP}/content/en/blog/post.md", "en", None),
        (f"{TOP}/content/en/docs/images/diagram.svg", "en", None),
        (f"{TOP}/README.md", "en", None),
        (f"{TOP}/content/en/docs/../../../evil.md", "en", None),
        (f"/{TOP}/content/en/docs/abs.md", "en", None),
    ],
)
def test_docs_relative_path(name: str, lang: str, expected: str | None) -> None:
    result = docs_relative_path(name, lang)
    assert (result.as_posix() if result else None) == expected


@pytest.mark.parametrize(
    ("path", "safe"),
    [("a/b.md", True), ("../a.md", False), ("a/../../b.md", False), ("C:/x.md", False)],
)
def test_is_safe_relative(path: str, safe: bool) -> None:
    assert is_safe_relative(PurePosixPath(path)) is safe


def test_extract_docs_writes_selected_files_and_manifest(tmp_path: Path) -> None:
    archive = make_archive(
        {
            f"{TOP}/content/en/docs/concepts/pods.md": b"# Pods",
            f"{TOP}/content/fr/docs/concepts/pods.md": b"# Pods (fr)",
            f"{TOP}/content/de/docs/concepts/pods.md": b"# Pods (de)",
            f"{TOP}/content/en/docs/../../../escape.md": b"evil",
            f"{TOP}/layouts/index.html": b"<html>",
        }
    )

    manifests = extract_docs(archive, version="1.33", langs=("en", "fr"), out_dir=tmp_path)

    assert (tmp_path / "v1.33/en/concepts/pods.md").read_bytes() == b"# Pods"
    assert (tmp_path / "v1.33/fr/concepts/pods.md").read_bytes() == b"# Pods (fr)"
    assert not (tmp_path / "v1.33/de").exists()
    assert not (tmp_path.parent / "escape.md").exists()
    assert not list(tmp_path.rglob("escape.md"))
    assert [f.path for f in manifests["en"].files] == ["concepts/pods.md"]

    saved = json.loads((tmp_path / "v1.33/en/manifest.json").read_text(encoding="utf-8"))
    assert saved["license"] == "CC-BY-4.0"
    assert saved["ref"] == "release-1.33"
    assert len(saved["files"][0]["sha256"]) == 64


@pytest.mark.parametrize("version", ["latest", "1.33; rm -rf /", "2.0", ""])
def test_download_rejects_invalid_versions(version: str, tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Invalid Kubernetes version"):
        download(version, ("en",), tmp_path)


def test_cli_rejects_invalid_language(tmp_path: Path) -> None:
    with pytest.raises(SystemExit):
        main(["--langs", "../etc", "--out", str(tmp_path)])
