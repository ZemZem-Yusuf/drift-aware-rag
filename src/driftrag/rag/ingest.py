"""Ingestion: corpus snapshot -> chunks -> embeddings -> a new index version.

Everything happens in the caller's transaction: if any step fails (checksum, embedding,
database), nothing is left behind, not even the empty partition. A version is only usable
after ``finalize_index_version`` has built its HNSW index and marked it ``ready``.

Usage::

    uv run driftrag-ingest --snapshot data/raw/k8s-docs/v1.33/en \\
        --snapshot data/raw/k8s-docs/v1.33/fr --name k8s-1.33
"""

from __future__ import annotations

import argparse
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

from sqlalchemy import Connection, text

from driftrag.db.registry import (
    IndexVersion,
    create_index_version,
    finalize_index_version,
    set_alias,
)
from driftrag.rag.chunking import Chunk, ChunkerConfig, chunk_page, parse_page
from driftrag.rag.corpus import CorpusIntegrityError, SourceDocument, read_snapshot
from driftrag.rag.embeddings import E5Embedder, Embedder, HashingEmbedder, to_pgvector


@dataclass(frozen=True)
class IngestReport:
    version: IndexVersion
    documents: int
    chunks: int


@dataclass(frozen=True)
class _PendingChunk:
    document_id: int
    lang: str
    chunk: Chunk


def upsert_document(conn: Connection, doc: SourceDocument, title: str) -> int:
    """Return the document's id, inserting it if new.

    A document is identified by (corpus, corpus_version, lang, path). If one exists with a
    *different* checksum, the snapshot changed without a new version label, which would silently
    mix two contents under one name, so it's refused.
    """
    row = conn.execute(
        text(
            """
            INSERT INTO rag.documents (corpus, corpus_version, lang, path, title, sha256)
            VALUES (:corpus, :version, :lang, :path, :title, :sha256)
            ON CONFLICT (corpus, corpus_version, lang, path)
            DO UPDATE SET title = EXCLUDED.title
            WHERE rag.documents.sha256 = EXCLUDED.sha256
            RETURNING id
            """
        ),
        {
            "corpus": doc.corpus,
            "version": doc.corpus_version,
            "lang": doc.lang,
            "path": doc.path,
            "title": title,
            "sha256": doc.sha256,
        },
    ).scalar_one_or_none()
    if row is None:
        raise CorpusIntegrityError(
            f"{doc.corpus} {doc.corpus_version} [{doc.lang}] {doc.path} is already stored with a "
            "different checksum; use a new corpus version label"
        )
    return int(row)


def _insert_batch(
    conn: Connection, version: IndexVersion, embedder: Embedder, batch: Sequence[_PendingChunk]
) -> None:
    vectors = embedder.embed_documents([p.chunk.content for p in batch])
    conn.execute(
        text(
            """
            INSERT INTO rag.chunks
                (index_version_id, document_id, ordinal, lang, heading_path, content, embedding)
            VALUES (:vid, :doc, :ordinal, :lang, :heading, :content, CAST(:embedding AS vector))
            """
        ),
        [
            {
                "vid": version.id,
                "doc": p.document_id,
                "ordinal": p.chunk.ordinal,
                "lang": p.lang,
                "heading": p.chunk.heading_path,
                "content": p.chunk.content,
                "embedding": to_pgvector(vector),
            }
            for p, vector in zip(batch, vectors, strict=True)
        ],
    )


def ingest(
    conn: Connection,
    documents: Iterable[SourceDocument],
    *,
    index_name: str,
    embedder: Embedder,
    config: ChunkerConfig,
    batch_size: int = 64,
) -> IngestReport:
    """Build a new, ready index version from ``documents``. Call inside a transaction."""
    version = create_index_version(
        conn,
        name=index_name,
        embedding_model=embedder.name,
        embedding_dim=embedder.dim,
        chunker_config={**config.model_dump(), "config_id": config.config_id},
    )
    document_count = 0
    chunk_count = 0
    pending: list[_PendingChunk] = []
    for doc in documents:
        title = parse_page(doc.text, fallback_title=doc.path).title
        document_id = upsert_document(conn, doc, title)
        document_count += 1
        for chunk in chunk_page(doc.text, config, fallback_title=doc.path):
            pending.append(_PendingChunk(document_id, doc.lang, chunk))
            if len(pending) >= batch_size:
                _insert_batch(conn, version, embedder, pending)
                chunk_count += len(pending)
                pending = []
    if pending:
        _insert_batch(conn, version, embedder, pending)
        chunk_count += len(pending)
    ready = finalize_index_version(conn, version.id)
    return IngestReport(version=ready, documents=document_count, chunks=chunk_count)


def main(argv: list[str] | None = None) -> None:
    from driftrag.config import get_settings
    from driftrag.db.engine import make_engine

    parser = argparse.ArgumentParser(description="Build a new index version from snapshots.")
    parser.add_argument("--snapshot", type=Path, action="append", required=True)
    parser.add_argument("--name", required=True, help="unique index version name")
    parser.add_argument(
        "--embedder",
        choices=["e5", "hashing"],
        default="e5",
        help="e5: multilingual model (needs `uv sync --extra embeddings`); hashing: baseline",
    )
    parser.add_argument("--dim", type=int, default=256, help="hashing embedder only")
    parser.add_argument("--max-chars", type=int, default=ChunkerConfig().max_chars)
    parser.add_argument("--overlap-chars", type=int, default=ChunkerConfig().overlap_chars)
    parser.add_argument(
        "--alias",
        choices=["active", "canary"],
        help="also point this alias at the new version, in the same transaction",
    )
    args = parser.parse_args(argv)

    embedder: Embedder = E5Embedder() if args.embedder == "e5" else HashingEmbedder(dim=args.dim)
    config = ChunkerConfig(max_chars=args.max_chars, overlap_chars=args.overlap_chars)
    documents = (doc for snapshot in args.snapshot for doc in read_snapshot(snapshot))
    engine = make_engine(get_settings().database_url.get_secret_value())
    with engine.begin() as conn:
        report = ingest(conn, documents, index_name=args.name, embedder=embedder, config=config)
        if args.alias:
            set_alias(conn, args.alias, report.version.id, reason=f"ingest {args.name}")
    print(
        f"index version {report.version.id} '{report.version.name}' ready: "
        f"{report.documents} documents, {report.chunks} chunks, "
        f"embedder {report.version.embedding_model}, chunker {config.config_id}"
        + (f"; alias '{args.alias}' now points to it" if args.alias else "")
    )


if __name__ == "__main__":
    main()
