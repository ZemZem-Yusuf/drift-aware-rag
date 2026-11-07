"""Inline the example files that Kubernetes doc pages include through Hugo shortcodes.

Pages show YAML manifests and other examples with shortcodes such as
``{{% code_sample file="pods/simple-pod.yaml" %}}`` (French pages use the older ``codenew``).
On the website, Hugo replaces them with the file's content. A plain Markdown pipeline only sees
the shortcode, so without this step every example is missing from the index, including the
exact field names (``envFrom``, ``configMapRef``, ``minAvailable``) that "how do I configure"
questions depend on.

Each shortcode becomes a labelled fenced code block::

    Example file `pods/simple-pod.yaml`:
    ```yaml
    ...file content...
    ```

The label puts the file name into the text, so keyword search can match it too. A shortcode
whose file can't be found is left as is; the chunker then removes it like any other shortcode.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import PurePosixPath

_SHORTCODE = re.compile(
    r"\{\{[<%]\s*(?:code_sample|codenew|code)\b(?P<attrs>[^}]*?)[>%]\}\}", re.DOTALL
)
_ATTR = re.compile(r'(\w+)="([^"]*)"')
_LANGUAGE_BY_SUFFIX = {".yml": "yaml", ".sh": "shell", ".py": "python", ".conf": "", ".cfg": ""}


@dataclass(frozen=True)
class Resolution:
    text: str
    resolved: int
    missing: list[str]


def normalise_sample_path(file: str) -> str:
    """Shortcode paths are relative to the examples root; some start with '/'."""
    return PurePosixPath(file.lstrip("/")).as_posix()


def resolve_code_samples(markdown: str, lookup: Callable[[str], str | None]) -> Resolution:
    """Replace sample shortcodes with the files ``lookup`` returns (by normalised path)."""
    resolved = 0
    missing: list[str] = []

    def replace(match: re.Match[str]) -> str:
        nonlocal resolved
        attrs = dict(_ATTR.findall(match.group("attrs")))
        file = attrs.get("file")
        if not file:
            return match.group(0)
        path = normalise_sample_path(file)
        content = lookup(path)
        if content is None:
            missing.append(path)
            return match.group(0)
        resolved += 1
        suffix = PurePosixPath(path).suffix
        language = attrs.get("language") or _LANGUAGE_BY_SUFFIX.get(suffix, suffix.lstrip("."))
        body = content.rstrip("\n")
        fence = "~~~~" if "```" in body else "```"  # don't let the file's own fences end ours
        return f"\nExample file `{path}`:\n{fence}{language}\n{body}\n{fence}\n"

    return Resolution(_SHORTCODE.sub(replace, markdown), resolved, missing)
