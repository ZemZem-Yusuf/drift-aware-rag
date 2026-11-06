# Drift-Aware RAG

[![ci](https://github.com/ZemZem-Yusuf/drift-aware-rag/actions/workflows/ci.yml/badge.svg)](https://github.com/ZemZem-Yusuf/drift-aware-rag/actions/workflows/ci.yml)

A RAG platform that notices when it's going stale. It detects drift across six layers (user queries, the source corpus, retrieval quality, answer quality, behaviour, and silent upstream model changes), finds the most likely root cause, and ships the fix (for example a re-index) behind an evaluation gate with canary rollout and automatic rollback.

> **Status: phase 0 (foundations).** Package layout, tooling, CI and the corpus downloader are in place. The RAG pipeline, detectors and results come next; there are no results yet, and this README will only show numbers backed by committed result files.

## Quick start

Requires Python 3.12 and [uv](https://docs.astral.sh/uv/).

```bash
uv sync                      # create .venv and install dependencies
uv run poe check             # lint, format check, type check, tests
uv run poe dev               # API on http://127.0.0.1:8010/docs
uv run poe corpus            # download Kubernetes docs v1.33 + v1.36 (en, fr) into data/raw
```

Docker (API + Postgres with pgvector):

```bash
cp .env.example .env         # then set POSTGRES_PASSWORD
docker compose -f deploy/compose.yaml --env-file .env --profile core up -d --build
```

`make <task>` works too on Linux/macOS.

## Layout

```
src/driftrag/   api · rag · telemetry · drift · remediation · agent · security · datasets
src/evalkit/    evaluation toolkit, kept independent of driftrag so other projects can reuse it
tests/          unit tests (integration tests with testcontainers come with the database layer)
deploy/         Dockerfile, compose.yaml
```

## Data

The corpus is two release snapshots of the [Kubernetes documentation](https://github.com/kubernetes/website) (CC BY 4.0), in English and French. Versions one year apart give real corpus drift: pages are added, removed and rewritten. Downloads are never committed; each snapshot has a `manifest.json` with a SHA-256 per file so experiments are reproducible.

## License

Apache-2.0
