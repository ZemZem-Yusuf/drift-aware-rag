# Lab notebook

A dated record of what was built, measured, learned and decided, including what went wrong.
Numbers link to the saved run or log they come from (see [experiments/README.md](../experiments/README.md)).

---

## 2026-11-06: Foundations

- Package layout, tooling (uv, ruff, mypy strict, pytest), CI (lint, types, tests, secret scan, dependency audit, Docker smoke test).
- Database schema: each index version is its own partition with HNSW and full-text indexes; `active`/`canary` aliases switch versions in one transaction ([ADR-0001](adr/0001-postgres-pgvector.md)).
- Retrieval metrics and reciprocal rank fusion with property-based tests.
- **Issue:** the CI secret scan failed on the first PR: `gitleaks-action` needs `pull-requests: read` on private repos. Fixed with a job-level permission.

## 2026-11-07: Ingestion, retrieval, generation, first end-to-end run

### Built
Markdown chunker for Hugo docs, verified corpus reader (SHA-256 per file), ingestion pipeline, multilingual E5 embedder (pinned revision, safetensors only), hybrid retriever, LLM gateway (cache → fallback → daily budget → LiteLLM), answer generation with verified citations, `POST /ask`.

### Issues found and fixed
| Issue | Evidence | Fix |
|---|---|---|
| Keyword search lost matches | stemmed words were stemmed again (`exposes` → `expos` → `expo`) | cast the OR query straight to `tsquery`; regression test |
| A retrieval test failed in CI | the two searches each put a different chunk first; RRF tied them | unambiguous test query; documented the tie behaviour |
| 13 CVEs in `filelock` (transitive) | `pip-audit` in CI | `filelock>=4.2.1`; LiteLLM resolved to 1.103.10, the newest release without a `filelock<4` cap |
| Every DB connection took ~10 s on Windows | measured: `localhost` 10.0 s vs `127.0.0.1` 0.1 s (IPv6 tried first) | use `127.0.0.1` |
| Port clash with other local services | 5432 and 8000 already in use | project uses 5433 (Postgres) and 8010 (API) |
| **A first ingestion run was reported as successful but saved nothing** | the exit code checked was the last command in a shell pipeline, not the ingestion's; the run was cut off when the database stopped, and its single transaction rolled back (by design) | always record the process's own exit code; ingestion now verifies files before starting and logs progress every 15 s |

### Ingestion of Kubernetes docs v1.33 (en + fr)
From the ingestion log (`data/logs/ingest-k8s-1.33-e5.log`, not committed) and the index snapshot in the E0 results:
- Corpus: 1,495 English pages (10.7 MB) and 275 French pages (1.6 MB), downloaded in 1 min 49 s.
- Index `k8s-1.33-e5`: **15,939 chunks** (13,910 en, 2,029 fr) from 1,655 documents; chunker `caf19343c281`.
- Log summary: `INGEST_EXIT_CODE=0 after 1843s`, i.e. **~8.6 chunks/s** end to end on a laptop CPU (E5-small). A full re-index takes about 30 minutes, which matters for remediation design (re-indexing is the most common fix).
- 115 documents produced no chunks. Likely empty section index pages; **to verify** (a page losing real content would be a chunker bug).

### E0: first end-to-end run ([annotations](../experiments/E0-smoke/annotations.md))
Run: `experiments/E0-smoke/results/20261107T100022Z-baseline.json` (commit `7d0608f`, clean tree).

| Question | Verdict |
|---|---|
| Restart all pods of a Deployment | ❌ wrong (retrieval miss) |
| Liveness vs readiness probe | ✅ |
| Limit CPU and memory | ⚠️ partly correct |
| Qu'est-ce qu'un Pod ? (fr) | ✅ |
| Capital of France (out of scope) | ✅ refused |

Observations from the live run (before caching):
- LLM latency 3.6 s to 6.6 s; the out-of-scope refusal took 0.6 s.
- The first request took 52 s because the E5 model loads on first use (cold start). To fix before any demo: load the model at startup.
- Output tokens were 761 to 1,565 for short answers. Gemini 2.5 counts hidden "thinking" tokens, which costs latency and quota; worth measuring with a capped thinking budget.

**Diagnosis of the wrong answer** (`results/20261107T100116Z-diagnose-restart.json`): for the natural question, the `kubectl rollout restart` page is not in vector search's top 200 and is #21 in keyword search, so #58 after fusion. For the query "kubectl rollout restart deployment" it is #1 in both. Vocabulary gap between task language and command reference pages.

### Decision
Don't tune by intuition. Next: build the **golden set** (~50 questions with known relevant chunks, including the hard cases above), compute baseline recall@5 / MRR / nDCG with confidence intervals, then test hypotheses H1–H4 one at a time against that baseline.

### Golden set v0 and evaluation tooling
- [Golden set](../golden/README.md): 34 drafted items (30 retrieval: 24 EN, 6 FR; 4 out-of-scope). Relevance per document + section so it survives re-indexing. Every reference was checked to exist in the index. **Awaiting human review**; only verified items will count.
- `driftrag-eval` scores the active index and saves the run with the golden file's checksum; `driftrag-golden` produces a review sheet with the real documentation excerpts.
- **Dry run on unreviewed drafts** (not reportable; `experiments/R1-retrieval/results/20261107T101408Z-baseline-drafts.json`): recall@5 0.63 [0.47, 0.78], recall@10 0.71, MRR 0.47, nDCG@10 0.51, n=30. 9 questions have no relevant section in the top 5, including the predicted vocabulary-gap cases (restart, taint, DaemonSet, node selector). The ±0.16 interval shows how little 30 questions can resolve.
- **Chunker observation:** auto-generated `kubectl` reference pages keep raw HTML option tables and empty `##` headings in chunks. Candidate fix (H5): strip HTML tables/tags during cleaning; measure its effect like the others.
