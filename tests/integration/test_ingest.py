import uuid
from collections.abc import Sequence
from pathlib import Path

import pytest
from sqlalchemy import Engine, text

from driftrag.rag.chunking import ChunkerConfig, chunk_page
from driftrag.rag.corpus import CorpusIntegrityError, read_snapshot
from driftrag.rag.embeddings import HashingEmbedder, to_pgvector
from driftrag.rag.ingest import ingest
from tests.snapshots import write_snapshot

pytestmark = pytest.mark.integration

PODS_EN = """---
title: Pods
---
Pods are the smallest deployable units of computing in Kubernetes.

## Restarting

Use kubectl rollout restart to restart the Pods of a Deployment.
"""

SERVICES_EN = """---
title: Service
---
A Service exposes an application running on a set of Pods as a network service.
"""

PODS_FR = """---
title: Pods
---
Les Pods sont les plus petites unités déployables dans Kubernetes. Les conteneurs d'un Pod
partagent le réseau et le stockage.
"""


def _name() -> str:
    return f"test-{uuid.uuid4().hex[:8]}"


def test_ingest_builds_a_ready_searchable_version(engine: Engine, tmp_path: Path) -> None:
    corpus_version = uuid.uuid4().hex[:6]
    en = write_snapshot(
        tmp_path, {"pods.md": PODS_EN, "svc.md": SERVICES_EN}, version=corpus_version
    )
    fr = write_snapshot(tmp_path, {"pods.md": PODS_FR}, version=corpus_version, lang="fr")
    embedder = HashingEmbedder(dim=128)
    config = ChunkerConfig(min_chars=0)
    documents = [*read_snapshot(en), *read_snapshot(fr)]

    with engine.begin() as conn:
        report = ingest(
            conn, documents, index_name=_name(), embedder=embedder, config=config, batch_size=2
        )

    expected_chunks = sum(len(chunk_page(d.text, config, fallback_title=d.path)) for d in documents)
    assert report.documents == 3
    assert report.chunks == expected_chunks
    assert report.version.status == "ready"
    assert report.version.embedding_model == "hashing-v1-128"

    with engine.connect() as conn:
        nearest = conn.execute(
            text(
                """
                SELECT heading_path FROM rag.chunks WHERE index_version_id = :vid
                ORDER BY embedding::vector(128) <=> CAST(:q AS vector(128)) LIMIT 1
                """
            ),
            {
                "vid": report.version.id,
                "q": to_pgvector(embedder.embed_query("how to restart pods with kubectl rollout")),
            },
        ).scalar_one()
        french_hits = conn.execute(
            text(
                """
                SELECT count(*) FROM rag.chunks WHERE index_version_id = :vid
                AND lang = 'fr' AND tsv @@ plainto_tsquery('french', 'conteneur')
                """
            ),
            {"vid": report.version.id},
        ).scalar_one()
        stored_config = conn.execute(
            text("SELECT chunker_config->>'config_id' FROM rag.index_versions WHERE id = :vid"),
            {"vid": report.version.id},
        ).scalar_one()
    assert nearest == "Pods > Restarting"
    assert french_hits == 1
    assert stored_config == config.config_id


def test_reingesting_reuses_documents(engine: Engine, tmp_path: Path) -> None:
    snapshot = write_snapshot(tmp_path, {"pods.md": PODS_EN}, version=uuid.uuid4().hex[:6])
    embedder = HashingEmbedder(dim=64)
    with engine.begin() as conn:
        first = ingest(
            conn,
            read_snapshot(snapshot),
            index_name=_name(),
            embedder=embedder,
            config=ChunkerConfig(),
        )
    with engine.begin() as conn:
        second = ingest(
            conn,
            read_snapshot(snapshot),
            index_name=_name(),
            embedder=embedder,
            config=ChunkerConfig(max_chars=600, overlap_chars=100),
        )

    with engine.connect() as conn:
        doc_ids = (
            conn.execute(
                text(
                    """
                SELECT DISTINCT document_id FROM rag.chunks
                WHERE index_version_id IN (:a, :b)
                """
                ),
                {"a": first.version.id, "b": second.version.id},
            )
            .scalars()
            .all()
        )
    assert len(doc_ids) == 1  # same document row, two index versions


def test_changed_content_under_same_version_label_is_refused_and_rolled_back(
    engine: Engine, tmp_path: Path
) -> None:
    corpus_version = uuid.uuid4().hex[:6]
    original = write_snapshot(tmp_path / "a", {"pods.md": PODS_EN}, version=corpus_version)
    changed = write_snapshot(
        tmp_path / "b", {"pods.md": PODS_EN + "\nNew text."}, version=corpus_version
    )
    embedder = HashingEmbedder(dim=64)
    with engine.begin() as conn:
        ingest(
            conn,
            read_snapshot(original),
            index_name=_name(),
            embedder=embedder,
            config=ChunkerConfig(),
        )

    failed_name = _name()
    with pytest.raises(CorpusIntegrityError, match="different checksum"), engine.begin() as conn:
        ingest(
            conn,
            read_snapshot(changed),
            index_name=failed_name,
            embedder=embedder,
            config=ChunkerConfig(),
        )

    with engine.connect() as conn:
        leftover = conn.execute(
            text("SELECT count(*) FROM rag.index_versions WHERE name = :n"), {"n": failed_name}
        ).scalar_one()
    assert leftover == 0  # the whole ingest, partition included, was rolled back


def test_progress_is_reported_after_each_batch(engine: Engine, tmp_path: Path) -> None:
    snapshot = write_snapshot(
        tmp_path, {"pods.md": PODS_EN, "svc.md": SERVICES_EN}, version=uuid.uuid4().hex[:6]
    )
    calls: list[tuple[int, int]] = []
    with engine.begin() as conn:
        report = ingest(
            conn,
            read_snapshot(snapshot),
            index_name=_name(),
            embedder=HashingEmbedder(dim=64),
            config=ChunkerConfig(min_chars=0),
            batch_size=1,
            progress=lambda docs, chunks: calls.append((docs, chunks)),
        )
    assert len(calls) == report.chunks  # one call per batch of one chunk
    assert calls == sorted(calls)  # counts only grow
    assert calls[-1] == (report.documents, report.chunks)


class RecordingEmbedder(HashingEmbedder):
    """Hashing embedder that remembers the texts it was asked to embed."""

    def __init__(self) -> None:
        super().__init__(dim=64)
        self.seen: list[str] = []

    def embed_documents(self, texts: Sequence[str]) -> list[list[float]]:
        self.seen.extend(texts)
        return super().embed_documents(texts)


def test_embed_headings_changes_only_the_embedding_input(engine: Engine, tmp_path: Path) -> None:
    snapshot = write_snapshot(tmp_path, {"pods.md": PODS_EN}, version=uuid.uuid4().hex[:6])
    embedder = RecordingEmbedder()
    with engine.begin() as conn:
        report = ingest(
            conn,
            read_snapshot(snapshot),
            index_name=_name(),
            embedder=embedder,
            config=ChunkerConfig(min_chars=0),
            embed_headings=True,
        )
    assert any(text.startswith("Pods > Restarting\n\n") for text in embedder.seen)

    with engine.connect() as conn:
        stored = conn.execute(
            text("SELECT content FROM rag.chunks WHERE index_version_id = :vid ORDER BY ordinal"),
            {"vid": report.version.id},
        ).scalars()
        recorded = conn.execute(
            text("SELECT chunker_config->>'embedding_input' FROM rag.index_versions WHERE id = :v"),
            {"v": report.version.id},
        ).scalar_one()
        expected = [
            c.content
            for c in chunk_page(PODS_EN, ChunkerConfig(min_chars=0), fallback_title="pods.md")
        ]
        assert list(stored) == expected  # stored text is the chunker's output, no heading added
    assert recorded == "heading_path+content"
