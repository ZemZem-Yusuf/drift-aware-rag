"""Index registry: immutable index versions and the aliases that point to them (ADR-0001).

Lifecycle of a version::

    create_index_version()   -> status 'building', empty partition rag.chunks_v{id}
    (bulk insert chunks)
    finalize_index_version() -> builds the HNSW index, status 'ready'
    set_alias('canary' | 'active', id)  -> one transaction, recorded in rag.alias_history
    rollback_alias('active')            -> points the alias back to its previous version

The HNSW index is built *after* the bulk insert because building it once is much faster than
updating it row by row. All functions take a Connection and expect the caller to manage the
transaction (``with engine.begin() as conn: ...``), so several steps can be made atomic.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Literal

from sqlalchemy import Connection, text

Alias = Literal["active", "canary"]
Status = Literal["building", "ready", "retired"]


class RegistryError(RuntimeError):
    """An operation that would break the registry's invariants."""


@dataclass(frozen=True)
class IndexVersion:
    id: int
    name: str
    embedding_model: str
    embedding_dim: int
    status: Status

    @property
    def partition(self) -> str:
        """Fully qualified partition name. Built from an integer id, so safe to inline in SQL."""
        return f"rag.chunks_v{int(self.id)}"


def _to_version(row: Any) -> IndexVersion:
    return IndexVersion(
        id=int(row.id),
        name=str(row.name),
        embedding_model=str(row.embedding_model),
        embedding_dim=int(row.embedding_dim),
        status=row.status,
    )


def create_index_version(
    conn: Connection,
    *,
    name: str,
    embedding_model: str,
    embedding_dim: int,
    chunker_config: Mapping[str, Any],
) -> IndexVersion:
    """Register a new version and create its empty partition with a full-text index."""
    row = conn.execute(
        text(
            """
            INSERT INTO rag.index_versions (name, embedding_model, embedding_dim, chunker_config)
            VALUES (:name, :model, :dim, CAST(:config AS jsonb))
            RETURNING id, name, embedding_model, embedding_dim, status
            """
        ),
        {
            "name": name,
            "model": embedding_model,
            "dim": embedding_dim,
            "config": json.dumps(dict(chunker_config), sort_keys=True),
        },
    ).one()
    version = _to_version(row)
    vid = version.id
    conn.execute(
        text(f"CREATE TABLE {version.partition} PARTITION OF rag.chunks FOR VALUES IN ({vid})")
    )
    conn.execute(text(f"CREATE INDEX chunks_v{vid}_tsv ON {version.partition} USING gin (tsv)"))
    return version


def get_index_version(conn: Connection, version_id: int) -> IndexVersion:
    row = conn.execute(
        text(
            "SELECT id, name, embedding_model, embedding_dim, status "
            "FROM rag.index_versions WHERE id = :id"
        ),
        {"id": version_id},
    ).one_or_none()
    if row is None:
        raise RegistryError(f"index version {version_id} does not exist")
    return _to_version(row)


def finalize_index_version(conn: Connection, version_id: int) -> IndexVersion:
    """Check every embedding has the version's dimension, build the HNSW index, mark ready."""
    version = get_index_version(conn, version_id)
    if version.status != "building":
        raise RegistryError(f"version {version_id} is '{version.status}', expected 'building'")
    dim = version.embedding_dim
    wrong = conn.execute(
        # Partition name is built from an integer id (see IndexVersion.partition): not injectable.
        text(f"SELECT count(*) FROM {version.partition} WHERE vector_dims(embedding) <> :dim"),  # noqa: S608
        {"dim": dim},
    ).scalar_one()
    if wrong:
        raise RegistryError(f"{wrong} chunk(s) in version {version_id} don't have dimension {dim}")
    conn.execute(
        text(
            f"CREATE INDEX chunks_v{version.id}_hnsw ON {version.partition} "
            f"USING hnsw ((embedding::vector({dim})) vector_cosine_ops)"
        )
    )
    conn.execute(
        text("UPDATE rag.index_versions SET status = 'ready' WHERE id = :id"), {"id": version.id}
    )
    return get_index_version(conn, version.id)


def resolve_alias(conn: Connection, alias: Alias) -> IndexVersion | None:
    row = conn.execute(
        text(
            """
            SELECT v.id, v.name, v.embedding_model, v.embedding_dim, v.status
            FROM rag.index_aliases a JOIN rag.index_versions v ON v.id = a.index_version_id
            WHERE a.alias = :alias
            """
        ),
        {"alias": alias},
    ).one_or_none()
    return None if row is None else _to_version(row)


def set_alias(conn: Connection, alias: Alias, version_id: int, *, reason: str) -> None:
    """Point ``alias`` at a ready version and record the change. Call inside a transaction."""
    if not reason.strip():
        raise RegistryError("a reason is required for every alias change (audit log)")
    version = get_index_version(conn, version_id)
    if version.status != "ready":
        raise RegistryError(f"version {version_id} is '{version.status}', only 'ready' can serve")
    current = conn.execute(
        text("SELECT index_version_id FROM rag.index_aliases WHERE alias = :alias FOR UPDATE"),
        {"alias": alias},
    ).scalar_one_or_none()
    if current == version_id:
        return
    conn.execute(
        text(
            """
            INSERT INTO rag.index_aliases (alias, index_version_id) VALUES (:alias, :vid)
            ON CONFLICT (alias)
            DO UPDATE SET index_version_id = EXCLUDED.index_version_id, updated_at = now()
            """
        ),
        {"alias": alias, "vid": version_id},
    )
    conn.execute(
        text(
            """
            INSERT INTO rag.alias_history (alias, from_version, to_version, reason)
            VALUES (:alias, :from_v, :to_v, :reason)
            """
        ),
        {"alias": alias, "from_v": current, "to_v": version_id, "reason": reason},
    )


def rollback_alias(conn: Connection, alias: Alias, *, reason: str) -> IndexVersion:
    """Point ``alias`` back to the version it pointed to before its last change."""
    previous = conn.execute(
        text(
            """
            SELECT from_version FROM rag.alias_history
            WHERE alias = :alias ORDER BY id DESC LIMIT 1
            """
        ),
        {"alias": alias},
    ).scalar_one_or_none()
    if previous is None:
        raise RegistryError(f"alias '{alias}' has no previous version to roll back to")
    set_alias(conn, alias, int(previous), reason=f"rollback: {reason}")
    return get_index_version(conn, int(previous))
