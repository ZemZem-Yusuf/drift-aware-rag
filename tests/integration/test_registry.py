import uuid
from collections.abc import Sequence

import pytest
from sqlalchemy import Connection, Engine, text

from driftrag.db.registry import (
    IndexVersion,
    RegistryError,
    create_index_version,
    finalize_index_version,
    resolve_alias,
    rollback_alias,
    set_alias,
)

pytestmark = pytest.mark.integration


def _vec(values: Sequence[float]) -> str:
    return "[" + ",".join(str(v) for v in values) + "]"


def _document(conn: Connection, lang: str = "en") -> int:
    return int(
        conn.execute(
            text(
                """
                INSERT INTO rag.documents (corpus, corpus_version, lang, path, sha256)
                VALUES ('test', '1.0', :lang, :path, repeat('a', 64)) RETURNING id
                """
            ),
            {"lang": lang, "path": f"{uuid.uuid4()}.md"},
        ).scalar_one()
    )


def _chunk(
    conn: Connection, version: IndexVersion, doc: int, ordinal: int, content: str, emb: str
) -> None:
    conn.execute(
        text(
            """
            INSERT INTO rag.chunks
                (index_version_id, document_id, ordinal, lang, content, embedding)
            SELECT :vid, :doc, :ord, d.lang, :content, CAST(:emb AS vector)
            FROM rag.documents d WHERE d.id = :doc
            """
        ),
        {"vid": version.id, "doc": doc, "ord": ordinal, "content": content, "emb": emb},
    )


def _ready_version(engine: Engine, dim: int = 3) -> IndexVersion:
    with engine.begin() as conn:
        version = create_index_version(
            conn,
            name=f"v-{uuid.uuid4().hex[:8]}",
            embedding_model="test-model",
            embedding_dim=dim,
            chunker_config={"max_chars": 1200},
        )
        doc = _document(conn)
        _chunk(conn, version, doc, 0, "Pods are the smallest deployable units", _vec([1, 0, 0]))
        _chunk(conn, version, doc, 1, "A Service exposes an application", _vec([0, 1, 0]))
        return finalize_index_version(conn, version.id)


def test_version_gets_its_own_partition_and_indexes(engine: Engine) -> None:
    version = _ready_version(engine)
    with engine.connect() as conn:
        indexes = set(
            conn.execute(
                text("SELECT indexname FROM pg_indexes WHERE tablename = :t"),
                {"t": f"chunks_v{version.id}"},
            ).scalars()
        )
    assert version.status == "ready"
    assert {f"chunks_v{version.id}_hnsw", f"chunks_v{version.id}_tsv"} <= indexes


def test_vector_and_full_text_search_work_on_a_version(engine: Engine) -> None:
    version = _ready_version(engine)
    with engine.connect() as conn:
        nearest = conn.execute(
            text(
                """
                SELECT content FROM rag.chunks WHERE index_version_id = :vid
                ORDER BY embedding::vector(3) <=> CAST(:q AS vector(3)) LIMIT 1
                """
            ),
            {"vid": version.id, "q": _vec([0.9, 0.1, 0])},
        ).scalar_one()
        keyword = conn.execute(
            text(
                """
                SELECT content FROM rag.chunks
                WHERE index_version_id = :vid AND tsv @@ plainto_tsquery('english', 'services')
                """
            ),
            {"vid": version.id},
        ).scalar_one()
    assert nearest.startswith("Pods")
    assert keyword.startswith("A Service")  # stemming: 'services' matches 'Service'


def test_french_chunks_use_french_stemming(engine: Engine) -> None:
    with engine.begin() as conn:
        version = create_index_version(
            conn,
            name=f"fr-{uuid.uuid4().hex[:8]}",
            embedding_model="m",
            embedding_dim=2,
            chunker_config={},
        )
        doc = _document(conn, lang="fr")
        _chunk(conn, version, doc, 0, "Les conteneurs partagent le réseau", _vec([1, 0]))
        match = conn.execute(
            text(
                """
                SELECT count(*) FROM rag.chunks
                WHERE index_version_id = :vid AND tsv @@ plainto_tsquery('french', 'conteneur')
                """
            ),
            {"vid": version.id},
        ).scalar_one()
    assert match == 1


def test_finalize_rejects_wrong_embedding_dimension(engine: Engine) -> None:
    with engine.begin() as conn:
        version = create_index_version(
            conn,
            name=f"bad-{uuid.uuid4().hex[:8]}",
            embedding_model="m",
            embedding_dim=3,
            chunker_config={},
        )
        _chunk(conn, version, _document(conn), 0, "x", _vec([1, 0]))
        with pytest.raises(RegistryError, match="dimension 3"):
            finalize_index_version(conn, version.id)


def test_alias_requires_a_ready_version_and_a_reason(engine: Engine) -> None:
    ready = _ready_version(engine)
    with engine.begin() as conn:
        building = create_index_version(
            conn,
            name=f"b-{uuid.uuid4().hex[:8]}",
            embedding_model="m",
            embedding_dim=3,
            chunker_config={},
        )
        with pytest.raises(RegistryError, match="only 'ready'"):
            set_alias(conn, "canary", building.id, reason="test")
        with pytest.raises(RegistryError, match="reason"):
            set_alias(conn, "canary", ready.id, reason=" ")


def test_promote_then_rollback_restores_previous_version(engine: Engine) -> None:
    v1 = _ready_version(engine)
    v2 = _ready_version(engine)
    with engine.begin() as conn:
        set_alias(conn, "active", v1.id, reason="initial")
    with engine.begin() as conn:
        set_alias(conn, "active", v2.id, reason="corpus refresh")
    with engine.connect() as conn:
        assert resolve_alias(conn, "active") == v2

    with engine.begin() as conn:
        restored = rollback_alias(conn, "active", reason="eval gate failed in canary")

    with engine.connect() as conn:
        assert restored == v1
        assert resolve_alias(conn, "active") == v1
        last = conn.execute(
            text(
                """
                SELECT from_version, to_version, reason FROM rag.alias_history
                WHERE alias = 'active' ORDER BY id DESC LIMIT 1
                """
            )
        ).one()
    assert (last.from_version, last.to_version) == (v2.id, v1.id)
    assert last.reason == "rollback: eval gate failed in canary"


def test_failed_promotion_leaves_alias_unchanged(engine: Engine) -> None:
    """A transaction that fails half-way must not leave the alias pointing somewhere new."""
    v1 = _ready_version(engine)
    v2 = _ready_version(engine)
    with engine.begin() as conn:
        set_alias(conn, "canary", v1.id, reason="initial")

    def promote_then_crash() -> None:
        with engine.begin() as conn:
            set_alias(conn, "canary", v2.id, reason="promote")
            raise RuntimeError("simulated crash after the alias update")

    with pytest.raises(RuntimeError, match="simulated"):
        promote_then_crash()

    with engine.connect() as conn:
        assert resolve_alias(conn, "canary") == v1
