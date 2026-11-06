"""RAG schema: documents, index versions, partitioned chunks, aliases.

Revision ID: 0001
Create Date: 2026-11-07

Design (ADR-0001):
- ``rag.chunks`` is partitioned by ``index_version_id``. Each index version gets its own
  partition with its own HNSW and full-text indexes, created by ``driftrag.db.registry``.
- ``embedding`` has no fixed dimension, so versions can use different embedding models
  (experiment E3). The HNSW index casts to the version's dimension.
- ``rag.index_aliases`` maps ``active`` / ``canary`` to a version; promotion and rollback are a
  single transaction, recorded in ``rag.alias_history``.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE SCHEMA IF NOT EXISTS rag")

    op.execute(
        """
        CREATE TABLE rag.documents (
            id              bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            corpus          text NOT NULL,
            corpus_version  text NOT NULL,
            lang            text NOT NULL CHECK (lang ~ '^[a-z]{2}(-[a-z]{2})?$'),
            path            text NOT NULL,
            title           text,
            sha256          char(64) NOT NULL,
            ingested_at     timestamptz NOT NULL DEFAULT now(),
            UNIQUE (corpus, corpus_version, lang, path)
        )
        """
    )

    op.execute(
        """
        CREATE TABLE rag.index_versions (
            id               integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            name             text NOT NULL UNIQUE,
            embedding_model  text NOT NULL,
            embedding_dim    integer NOT NULL CHECK (embedding_dim BETWEEN 1 AND 4096),
            chunker_config   jsonb NOT NULL,
            status           text NOT NULL DEFAULT 'building'
                             CHECK (status IN ('building', 'ready', 'retired')),
            created_at       timestamptz NOT NULL DEFAULT now()
        )
        """
    )

    # Identity columns aren't allowed on partitioned tables before Postgres 17: use a sequence.
    op.execute("CREATE SEQUENCE rag.chunks_id_seq AS bigint")
    op.execute(
        """
        CREATE TABLE rag.chunks (
            index_version_id  integer NOT NULL REFERENCES rag.index_versions (id),
            id                bigint NOT NULL DEFAULT nextval('rag.chunks_id_seq'),
            document_id       bigint NOT NULL REFERENCES rag.documents (id),
            ordinal           integer NOT NULL CHECK (ordinal >= 0),
            lang              text NOT NULL,
            heading_path      text NOT NULL DEFAULT '',
            content           text NOT NULL,
            embedding         vector NOT NULL,
            tsv               tsvector GENERATED ALWAYS AS (
                                  to_tsvector(
                                      CASE WHEN lang = 'fr' THEN 'french'::regconfig
                                           ELSE 'english'::regconfig END,
                                      heading_path || ' ' || content
                                  )
                              ) STORED,
            PRIMARY KEY (index_version_id, id),
            UNIQUE (index_version_id, document_id, ordinal)
        ) PARTITION BY LIST (index_version_id)
        """
    )
    op.execute("ALTER SEQUENCE rag.chunks_id_seq OWNED BY rag.chunks.id")

    op.execute(
        """
        CREATE TABLE rag.index_aliases (
            alias             text PRIMARY KEY CHECK (alias IN ('active', 'canary')),
            index_version_id  integer NOT NULL REFERENCES rag.index_versions (id),
            updated_at        timestamptz NOT NULL DEFAULT now()
        )
        """
    )

    op.execute(
        """
        CREATE TABLE rag.alias_history (
            id            bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
            alias         text NOT NULL,
            from_version  integer REFERENCES rag.index_versions (id),
            to_version    integer NOT NULL REFERENCES rag.index_versions (id),
            reason        text NOT NULL CHECK (length(reason) > 0),
            changed_at    timestamptz NOT NULL DEFAULT now()
        )
        """
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS rag.alias_history")
    op.execute("DROP TABLE IF EXISTS rag.index_aliases")
    op.execute("DROP TABLE IF EXISTS rag.chunks CASCADE")
    op.execute("DROP SEQUENCE IF EXISTS rag.chunks_id_seq")
    op.execute("DROP TABLE IF EXISTS rag.index_versions")
    op.execute("DROP TABLE IF EXISTS rag.documents")
    op.execute("DROP SCHEMA IF EXISTS rag")
