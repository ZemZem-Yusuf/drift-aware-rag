# ADR-0001: PostgreSQL + pgvector as the single data store

- **Status:** Accepted
- **Date:** 2026-11-05
- **Deciders:** Youssef Zemzem

## Context

The system needs to store and query:

1. Chunk embeddings for retrieval (expected scale: 10k–500k vectors of 384–1024 dimensions).
2. Keyword search over the same chunks, for hybrid retrieval.
3. Interaction logs (queries, answers, scores, versions) for drift statistics.
4. The **index registry**: immutable index versions with `active` and `canary` aliases.
5. Drift events, remediation proposals and the audit log.

Requirement 4 drives the decision. Promoting or rolling back an index version must be **atomic**: at no moment can a request see a half-switched index, and rollback must restore the previous version exactly.

Constraints: open source, runs on a 16 GB laptop next to the rest of the stack, available as a managed service with a free tier for the cloud demo (Neon serverless Postgres supports pgvector; Azure and AWS also offer managed Postgres with pgvector).

## Options considered

| Option | Strengths | Weaknesses for this project |
|---|---|---|
| **A. PostgreSQL + pgvector + built-in full-text search** | One service; ACID transactions across vectors, logs and registry; HNSW index; SQL joins between logs and chunk metadata; available as a managed service on every major cloud; most widely used open-source database | Full-text ranking is weaker than BM25 in Elasticsearch; vector search scales less far than dedicated engines |
| B. Postgres + **Qdrant** | Fast filtered vector search, good developer experience | Two systems: alias swap can't be one transaction across both; more RAM; more failure modes |
| C. Postgres + **Milvus** | Built for billions of vectors, distributed | Heavy (etcd, object storage); far beyond the needed scale |
| D. **Elasticsearch / OpenSearch** for vectors + BM25 | Strong BM25 and hybrid search | JVM memory footprint; logs and registry still need a relational store; more ops |
| E. Pinecone | Fully managed | Not open source; adds vendor dependency and cost |

## Decision

Use **PostgreSQL 16 with pgvector** (HNSW, cosine distance) and Postgres full-text search (`tsvector` + GIN index) for hybrid retrieval. Logs, the index registry, drift events and the audit log live in the same database, in separate schemas.

**Blue/green index versions:** each index build writes to its own table (or partition) `chunks_v{N}`. A small `index_aliases` table maps `active` and `canary` to a version. Promotion and rollback are a single `UPDATE` inside a transaction. The retriever resolves the alias per request.

Access goes through a `Retriever` interface, so the vector backend can be replaced without touching the pipeline.

## Consequences

**Positive**
- Atomic promote and rollback, verified by an integration test (testcontainers).
- One backup, one connection pool, one service to monitor.
- Drift queries can join logs with chunk metadata in SQL.
- Same engine locally and in the cloud (Neon for the always-on demo).

**Negative / accepted risks**
- Postgres full-text ranking is not true BM25. Mitigation: hybrid fusion (reciprocal rank fusion) plus a cross-encoder reranker, measured in the eval set. Revisit if keyword recall is the bottleneck.
- HNSW index builds use memory. Mitigation: build new versions offline in the remediation flow, not on the request path.

**When to revisit**
- Corpus grows past ~10M vectors, or p95 retrieval latency exceeds the SLO under expected load → benchmark Qdrant/Milvus behind the same `Retriever` interface.
- Keyword recall measured as the main failure mode → add OpenSearch for BM25 only.

## Validation

- Integration test: promote, rollback, and concurrent reads during a swap never see a missing or mixed version.
- Benchmark (Phase 1): recall@10 and p95 latency of HNSW vs exact search on the golden set, recorded in `docs/results.md`.
