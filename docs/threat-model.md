# Threat Model (v0)

- **Status:** Draft v0. Updated at the end of each phase as components are built.
- **Method:** STRIDE per component, mapped to the [OWASP Top 10 for LLM Applications (2025)](https://genai.owasp.org/llm-top-10/).
- **Scope:** the local stack and the cloud demo. Only public data (Kubernetes documentation, synthetic queries) is processed.

## 1. What makes this system different

A normal RAG app reads a corpus that humans curate. This system **updates itself**: when it detects drift, it can re-index changed sources automatically. That creates two risks a normal RAG app doesn't have:

1. **The self-updating loop is an automated way to ingest attacker-controlled text.** If a watched source is compromised, poisoned content reaches the index without a human looking at it.
2. **The drift signals themselves can be manipulated.** An attacker who floods unusual queries can trigger expensive remediation, or hide real drift by shaping the traffic.

Most of the controls below exist because of these two risks.

## 2. Components and trust boundaries

```
 [User / client] ──(1)──► [API] ──► [Retriever] ──► [Postgres + pgvector]
                            │            ▲
                            ▼            │ (3) index versions
                       [LLM provider] ◄──┤ (2) external, untrusted output
                                         │
 [Watched sources] ──(4)──► [Ingestion] ─┘
                                 ▲
 [Scheduler] ──► [Drift checks] ──► [Policy engine] ──► [Remediation] ──(5)──► [Human approval]
                                                              │
                                                       [Audit log]
```

Trust boundaries: (1) the public API; (2) responses from external LLM providers; (3) the index registry, where versions are promoted; (4) external content entering ingestion; (5) the human approval step for costly actions.

## 3. Threats and controls

| # | Threat (STRIDE) | OWASP LLM | Where | Control | Status |
|---|---|---|---|---|---|
| T1 | **Poisoned documents** enter the index through automated re-indexing (Tampering) | LLM04 Data and model poisoning | Ingestion | Source allowlist; SHA-256 per document and provenance per chunk; injection/risk scan at ingestion; risky or large changes go to **quarantine** and need human approval | Planned (phase 5) |
| T2 | **Indirect prompt injection**: retrieved text contains instructions ("ignore previous instructions…") (Tampering, Elevation) | LLM01 Prompt injection | Generation | Retrieved text is wrapped and marked as data, never as instructions; output check for instruction-following; red-team cases with injected documents | Planned (phase 1 wrapping, phase 5 tests) |
| T3 | **Drift-signal manipulation**: flood of crafted queries triggers costly remediation or masks real drift (DoS, Tampering) | LLM10 Unbounded consumption | Drift checks | Per-key rate limits; traffic-source anomaly filter before drift statistics; cooldowns and budget caps on remediation; costly actions always need a human | Planned (phases 3–4) |
| T4 | **Bad remediation shipped**: a new index or config makes answers worse (Tampering) | — | Remediation | Immutable versions; eval gate before promotion; canary; automatic rollback; audit log | Planned (phase 4) |
| T5 | **Excessive agency**: the incident agent takes actions it shouldn't (Elevation) | LLM06 Excessive agency | Agent | Read-only allowlisted tools; the agent can only *draft* proposals; a human executes; every tool call is audited | Planned (phase 5) |
| T6 | **Sensitive data in logs or embeddings** (Information disclosure) | LLM02 Sensitive information disclosure | Telemetry | PII redaction before logging queries; embeddings treated as sensitive (they can leak content); retention limits; public data only in free tiers | Planned (phase 2) |
| T7 | **System prompt leakage** (Information disclosure) | LLM07 System prompt leakage | Generation | No secrets in prompts; leakage probes in the red-team suite | Planned (phase 5) |
| T8 | **Unsafe output handling**: model output rendered or executed downstream (Tampering) | LLM05 Improper output handling | API | Strict response schema; escape before any rendering; no output is ever executed | Planned (phase 1) |
| T9 | **Supply chain**: vulnerable or malicious dependency, model file or base image (Tampering) | LLM03 Supply chain | Build | Locked dependencies (`uv.lock`); `pip-audit` in CI; secret scanning (gitleaks); model weights pinned by name and revision, `safetensors` only, never unpickle untrusted files; image scanning (planned) | **Partly in place** (lockfile, pip-audit, gitleaks) |
| T10 | **Malicious archive** writes files outside the data folder during corpus download (Tampering) | LLM03 | Datasets | Streamed reading with an allowlist of paths; rejects absolute paths, `..`, drive letters and symlinks; size cap per file; tests with a crafted archive | **In place** (phase 0) |
| T11 | **Credential leakage**: database password or API keys in logs, images or git (Information disclosure) | LLM02 | Config | Secrets masked in settings (`SecretStr`); `.env` git-ignored; no default database password; gitleaks in CI | **In place** (phase 0) |
| T12 | **Exposed services** on the local network (Information disclosure) | — | Deploy | Postgres and API bound to `127.0.0.1`; containers run as non-root | **In place** (phase 0) |
| T13 | **API abuse / cost exhaustion** through the public API (DoS) | LLM10 | API | API keys with scopes; request size and token limits; rate limits; daily LLM budget in the gateway | Planned (phases 1–2) |

## 4. Out of scope (v0)

- Multi-tenant isolation (single tenant in this project).
- Attacks on the LLM providers themselves.
- Physical or host-level attacks on the machine running the stack.

## 5. Verification plan

- Unit tests for each in-place control (already in `tests/unit`).
- Red-team suite (promptfoo) in CI from phase 5: injection, poisoned documents, PII extraction, prompt leakage, with a pass-rate floor.
- Poisoning experiment: plant malicious documents in a corpus version and report the quarantine catch rate.
