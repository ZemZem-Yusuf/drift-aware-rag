"""Drift-Aware RAG: a RAG platform that detects drift and ships fixes behind an eval gate."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("drift-aware-rag")
except PackageNotFoundError:  # pragma: no cover - only when running from a source tree
    __version__ = "0.0.0"

__all__ = ["__version__"]
