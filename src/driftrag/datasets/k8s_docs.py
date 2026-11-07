"""Download versioned snapshots of the Kubernetes documentation (CC BY 4.0).

Two release snapshots give the project *real* corpus drift: pages are added, removed and
rewritten between versions, so a stale index produces genuinely wrong answers.

Usage::

    uv run driftrag-corpus --versions 1.33 1.36 --langs en fr --out data/raw

Each snapshot is written to ``<out>/k8s-docs/v<version>/<lang>/...`` with a ``manifest.json``
recording the source URL, git ref, license and a SHA-256 per file, so experiments can prove
which corpus they ran on.

The archive is read as a stream and only two kinds of files are kept: Markdown pages under
``content/<lang>/docs/``, and the example files under ``content/<lang>/examples/`` that pages
include through ``code_sample`` shortcodes (YAML manifests and similar, stored in
``<snapshot>/_examples/`` and listed separately in the manifest). Paths are validated before
writing (no absolute paths, no ``..``), because an archive is untrusted input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tarfile
import urllib.request
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path, PurePosixPath
from typing import IO

SOURCE_REPO = "https://github.com/kubernetes/website"
ARCHIVE_URL = "https://codeload.github.com/kubernetes/website/tar.gz/refs/heads/release-{version}"
LICENSE = "CC-BY-4.0"
DEFAULT_VERSIONS = ("1.33", "1.36")
DEFAULT_LANGS = ("en", "fr")
MAX_FILE_BYTES = 2 * 1024 * 1024
_VERSION_RE = re.compile(r"^1\.\d{1,3}$")
_LANG_RE = re.compile(r"^[a-z]{2}(-[a-z]{2})?$")


@dataclass(frozen=True)
class FileEntry:
    path: str
    sha256: str
    bytes: int


@dataclass
class Manifest:
    source: str
    ref: str
    version: str
    lang: str
    license: str
    retrieved_at: str
    files: list[FileEntry] = field(default_factory=list)
    examples: list[FileEntry] = field(default_factory=list)


EXAMPLES_DIR = "_examples"
EXAMPLE_SUFFIXES = frozenset(
    {".yaml", ".yml", ".json", ".conf", ".py", ".sh", ".txt", ".toml", ".properties", ".cfg"}
)


def _content_relative_path(
    member_name: str, lang: str, subdir: str, suffixes: frozenset[str]
) -> PurePosixPath | None:
    parts = PurePosixPath(member_name).parts
    if len(parts) < 5 or member_name.startswith("/"):
        return None
    _top, content, member_lang, directory, *rest = parts
    if (content, member_lang, directory) != ("content", lang, subdir):
        return None
    relative = PurePosixPath(*rest)
    if relative.suffix not in suffixes or not is_safe_relative(relative):
        return None
    return relative


def docs_relative_path(member_name: str, lang: str) -> PurePosixPath | None:
    """Map an archive member name to its path below ``content/<lang>/docs/``.

    Returns ``None`` for anything that isn't a Markdown doc page in that language, or whose
    path is unsafe. Archive names look like ``website-release-1.33/content/en/docs/a/b.md``.
    """
    return _content_relative_path(member_name, lang, "docs", frozenset({".md"}))


def examples_relative_path(member_name: str, lang: str) -> PurePosixPath | None:
    """Map an archive member name to its path below ``content/<lang>/examples/``."""
    return _content_relative_path(member_name, lang, "examples", EXAMPLE_SUFFIXES)


def is_safe_relative(path: PurePosixPath) -> bool:
    """True if ``path`` stays inside its target directory once joined to it."""
    return (
        not path.is_absolute()
        and all(part not in ("..", "") for part in path.parts)
        and ":" not in str(path)  # blocks Windows drive letters and alternate data streams
    )


def extract_docs(
    archive: IO[bytes], *, version: str, langs: tuple[str, ...], out_dir: Path
) -> dict[str, Manifest]:
    """Stream a gzipped tar archive and write the selected docs. Returns one manifest per lang."""
    retrieved_at = datetime.now(UTC).isoformat(timespec="seconds")
    manifests = {
        lang: Manifest(
            source=SOURCE_REPO,
            ref=f"release-{version}",
            version=version,
            lang=lang,
            license=LICENSE,
            retrieved_at=retrieved_at,
        )
        for lang in langs
    }
    with tarfile.open(fileobj=archive, mode="r|gz") as tar:
        for member in tar:
            if not member.isfile() or member.size > MAX_FILE_BYTES:
                continue
            for lang in langs:
                relative = docs_relative_path(member.name, lang)
                is_example = False
                if relative is None:
                    relative = examples_relative_path(member.name, lang)
                    is_example = True
                if relative is None:
                    continue
                handle = tar.extractfile(member)
                if handle is None:  # pragma: no cover - isfile() members always have data
                    continue
                data = handle.read()
                snapshot = out_dir / f"v{version}" / lang
                target = (snapshot / EXAMPLES_DIR if is_example else snapshot).joinpath(
                    *relative.parts
                )
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)
                entry = FileEntry(
                    path=relative.as_posix(),
                    sha256=hashlib.sha256(data).hexdigest(),
                    bytes=len(data),
                )
                (manifests[lang].examples if is_example else manifests[lang].files).append(entry)
                break
    for lang, manifest in manifests.items():
        manifest.files.sort(key=lambda entry: entry.path)
        manifest.examples.sort(key=lambda entry: entry.path)
        manifest_path = out_dir / f"v{version}" / lang / "manifest.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(asdict(manifest), indent=2), encoding="utf-8")
    return manifests


def download(version: str, langs: tuple[str, ...], out_dir: Path) -> dict[str, Manifest]:
    if not _VERSION_RE.match(version):
        raise ValueError(f"Invalid Kubernetes version: {version!r} (expected e.g. '1.33')")
    url = ARCHIVE_URL.format(version=version)
    request = urllib.request.Request(url, headers={"User-Agent": "drift-aware-rag-corpus"})  # noqa: S310 - fixed https URL
    with urllib.request.urlopen(request, timeout=120) as response:  # noqa: S310 - fixed https URL
        return extract_docs(response, version=version, langs=langs, out_dir=out_dir)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0] if __doc__ else None)
    parser.add_argument("--versions", nargs="+", default=list(DEFAULT_VERSIONS))
    parser.add_argument("--langs", nargs="+", default=list(DEFAULT_LANGS))
    parser.add_argument("--out", type=Path, default=Path("data/raw"))
    args = parser.parse_args(argv)

    langs = tuple(args.langs)
    if bad := [lang for lang in langs if not _LANG_RE.match(lang)]:
        parser.error(f"invalid language code(s): {bad}")
    out_dir: Path = args.out / "k8s-docs"
    for version in args.versions:
        manifests = download(version, langs, out_dir)
        for lang, manifest in manifests.items():
            total = sum(entry.bytes for entry in manifest.files)
            print(
                f"v{version} [{lang}]: {len(manifest.files)} pages, {total / 1e6:.1f} MB, "
                f"{len(manifest.examples)} example files"
            )


if __name__ == "__main__":
    main()
