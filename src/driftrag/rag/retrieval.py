"""Hybrid retrieval over the index version an alias points to.

For one query:

1. Resolve the alias (``active`` or ``canary``) to an index version, and refuse to search if
   the version was built with a different embedding model than the one we query with: vectors
   from two models live in different spaces, so the similarity scores would be meaningless.
2. **Vector search**: nearest chunks by cosine distance (HNSW index of that version).
3. **Keyword search**: Postgres full-text search with the query's language (stemming and stop
   words), ranked by ``ts_rank_cd``. Query terms are joined with OR, not AND: a natural
   question rarely shares *every* word with the right chunk, and the ranking already favours
   chunks that match more terms.
4. Fuse the two candidate lists with reciprocal rank fusion and return the top ``k``, with both
   original ranks kept for debugging and evaluation ("was this found by vectors, keywords or
   both?").
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

from sqlalchemy import Connection, Engine, text

from driftrag.db.registry import Alias, IndexVersion, resolve_alias
from driftrag.rag.embeddings import Embedder, to_pgvector
from driftrag.rag.fusion import reciprocal_rank_fusion
from driftrag.rag.rerank import Reranker

Lang = Literal["en", "fr"]
_TEXT_SEARCH_CONFIG: dict[Lang, str] = {"en": "english", "fr": "french"}


class RetrievalError(RuntimeError):
    """The retriever can't serve this request (no index, wrong embedding model, ...)."""


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: int
    document_path: str
    heading_path: str
    lang: str
    content: str
    score: float
    vector_rank: int | None
    keyword_rank: int | None
    rerank_score: float | None = None


@dataclass(frozen=True)
class RetrievalResult:
    index_version: IndexVersion
    chunks: list[RetrievedChunk]


class HybridRetriever:
    def __init__(
        self,
        engine: Engine,
        embedder: Embedder,
        *,
        alias: Alias = "active",
        candidates: int = 50,
        rrf_k: int = 60,
        weights: tuple[float, float] = (1.0, 1.0),
        reranker: Reranker | None = None,
        rerank_depth: int = 30,
        rerank_with_heading: bool = True,
    ) -> None:
        if candidates <= 0:
            raise ValueError("candidates must be positive")
        if rerank_depth <= 0:
            raise ValueError("rerank_depth must be positive")
        self._engine = engine
        self._embedder = embedder
        self._alias: Alias = alias
        self._candidates = candidates
        self._rrf_k = rrf_k
        self._weights = weights
        self._reranker = reranker
        self._rerank_depth = rerank_depth
        self._rerank_with_heading = rerank_with_heading

    def search(self, query: str, *, lang: Lang = "en", top_k: int = 5) -> RetrievalResult:
        if not query.strip():
            raise ValueError("query must not be empty")
        if top_k <= 0:
            raise ValueError("top_k must be positive")
        query_vector = self._embedder.embed_query(query)
        # One transaction so SET LOCAL applies and both searches see the same alias target.
        with self._engine.begin() as conn:
            version = self._version(conn)
            # HNSW returns approximate neighbours; a larger candidate list keeps recall high
            # when the language filter removes some of them.
            ef_search = max(40, min(1000, self._candidates * 2))
            conn.execute(text(f"SET LOCAL hnsw.ef_search = {ef_search}"))
            vector_ids = self._vector_search(conn, version, query_vector, lang)
            keyword_ids = self._keyword_search(conn, version, query, lang)
            fused = reciprocal_rank_fusion(
                [[str(i) for i in vector_ids], [str(i) for i in keyword_ids]],
                k=self._rrf_k,
                weights=list(self._weights),
            )
            depth = max(top_k, self._rerank_depth) if self._reranker else top_k
            chunks = self._load(conn, version, fused[:depth], vector_ids, keyword_ids)
        if self._reranker is not None:
            chunks = self._rerank(query, chunks)
        return RetrievalResult(index_version=version, chunks=chunks[:top_k])

    def _rerank(self, query: str, chunks: list[RetrievedChunk]) -> list[RetrievedChunk]:
        """Re-order candidates by cross-encoder score; ties keep the fused order."""
        if self._reranker is None or not chunks:
            return chunks
        passages = [
            f"{c.heading_path}\n{c.content}" if self._rerank_with_heading else c.content
            for c in chunks
        ]
        scores = self._reranker.score(query, passages)
        scored = [replace(c, rerank_score=s) for c, s in zip(chunks, scores, strict=True)]
        order = sorted(range(len(scored)), key=lambda i: (-scores[i], i))
        return [scored[i] for i in order]

    def _version(self, conn: Connection) -> IndexVersion:
        version = resolve_alias(conn, self._alias)
        if version is None:
            raise RetrievalError(f"alias '{self._alias}' doesn't point to any index version")
        if version.embedding_model != self._embedder.name:
            raise RetrievalError(
                f"index version {version.id} was built with '{version.embedding_model}' but the "
                f"query embedder is '{self._embedder.name}'; vectors from different models "
                "can't be compared"
            )
        return version

    def _vector_search(
        self, conn: Connection, version: IndexVersion, vector: list[float], lang: Lang
    ) -> list[int]:
        dim = int(version.embedding_dim)  # integer from the registry: safe to inline
        rows = conn.execute(
            text(
                f"""
                SELECT id FROM rag.chunks
                WHERE index_version_id = :vid AND lang = :lang
                ORDER BY embedding::vector({dim}) <=> CAST(:q AS vector({dim}))
                LIMIT :n
                """  # noqa: S608 - only the integer dimension is interpolated
            ),
            {"vid": version.id, "lang": lang, "q": to_pgvector(vector), "n": self._candidates},
        )
        return [int(r) for r in rows.scalars()]

    def _keyword_search(
        self, conn: Connection, version: IndexVersion, query: str, lang: Lang
    ) -> list[int]:
        rows = conn.execute(
            text(
                """
                SELECT id FROM rag.chunks,
                     -- plainto_tsquery stems once and joins with '&'. Swap to '|' and cast the
                     -- text straight to tsquery: to_tsquery() would stem the stems again, and
                     -- stemming isn't idempotent ('exposes' -> 'expos' -> 'expo').
                     CAST(
                         replace(plainto_tsquery(CAST(:config AS regconfig), :query)::text,
                                 ' & ', ' | ')
                         AS tsquery
                     ) AS q
                WHERE index_version_id = :vid AND lang = :lang AND tsv @@ q
                ORDER BY ts_rank_cd(tsv, q) DESC, id
                LIMIT :n
                """
            ),
            {
                "config": _TEXT_SEARCH_CONFIG[lang],
                "query": query,
                "vid": version.id,
                "lang": lang,
                "n": self._candidates,
            },
        )
        return [int(r) for r in rows.scalars()]

    def _load(
        self,
        conn: Connection,
        version: IndexVersion,
        fused: list[tuple[str, float]],
        vector_ids: list[int],
        keyword_ids: list[int],
    ) -> list[RetrievedChunk]:
        if not fused:
            return []
        ids = [int(doc_id) for doc_id, _ in fused]
        rows = conn.execute(
            text(
                """
                SELECT c.id, d.path, c.heading_path, c.lang, c.content
                FROM rag.chunks c JOIN rag.documents d ON d.id = c.document_id
                WHERE c.index_version_id = :vid AND c.id = ANY(:ids)
                """
            ),
            {"vid": version.id, "ids": ids},
        ).all()
        by_id = {int(r.id): r for r in rows}
        vector_rank = {chunk_id: rank for rank, chunk_id in enumerate(vector_ids, start=1)}
        keyword_rank = {chunk_id: rank for rank, chunk_id in enumerate(keyword_ids, start=1)}
        return [
            RetrievedChunk(
                chunk_id=chunk_id,
                document_path=str(by_id[chunk_id].path),
                heading_path=str(by_id[chunk_id].heading_path),
                lang=str(by_id[chunk_id].lang),
                content=str(by_id[chunk_id].content),
                score=score,
                vector_rank=vector_rank.get(chunk_id),
                keyword_rank=keyword_rank.get(chunk_id),
            )
            for chunk_id, score in ((int(doc_id), score) for doc_id, score in fused)
        ]
