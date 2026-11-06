# ADR-0003: Fix drift by remediation, not by retraining the model

- **Status:** Proposed
- **Date:** 2026-11-07
- **Deciders:** Youssef Zemzem

## Context

The original project idea was a "drift-aware **retraining** pipeline": when drift is detected, fine-tune the model. In a RAG system, most quality drops have causes that fine-tuning can't fix:

| Cause | Example | Does fine-tuning help? |
|---|---|---|
| Stale index | The docs changed, the index still has the old version | No. The model would learn outdated facts. |
| Retrieval config | Users now ask shorter, keyword-style questions; vector-only search misses them | No |
| Prompt regression | A prompt edit made answers worse | No |
| New topics | Users ask about features the corpus never covered | No. The content must be ingested. |
| Upstream model change | The provider silently updated the model | Partly, but you usually can't fine-tune a hosted model you don't control |

Fine-tuning is also slow, costly, needs labelled data, and is hard to roll back.

## Options considered

| Option | Cost | Time to apply | Reversible? | Fixes |
|---|---|---|---|---|
| A. **Re-index** changed sources (blue/green index version) | Low (embedding compute) | Minutes | Yes: switch the alias back | Corpus drift (L2), part of retrieval drift (L3) |
| B. **Retrieval tuning** (hybrid weight, top-k, reranker), searched against the eval set | Low | Minutes | Yes: config version | Retrieval drift (L3), part of query drift (L1) |
| C. **Prompt rollback** to the last good version | None | Seconds | Yes | Answer drift caused by a prompt change (L4) |
| D. **Targeted ingestion** of missing content (coverage-gap report → human adds sources) | Human time | Days | Yes | New topics (L1) |
| E. **Pin or switch the model version** | Varies | Minutes | Yes | Upstream change (L6) |
| F. **Fine-tune** (e.g. LoRA adapter) | High | Hours to days | Harder | Style or format problems the prompt can't fix |

## Decision

> _To be written by the author._
>
> Proposed direction: a **remediation playbook ordered by cost and reversibility** (C → B → A → E → D). Every automated action produces a new immutable version and passes the eval gate before it's promoted. Fine-tuning (F) is out of scope for v1 and only kept as a documented stretch option.

## Consequences

> _To be written with the decision._ Points to cover: what the system can fix automatically vs what needs a human; why "remediation" is the better name for the project's loop; what's lost by not fine-tuning.

## When to revisit

- The eval set shows a persistent quality gap that no retrieval, prompt or content change closes, and the gap is about style or format → evaluate a LoRA adapter as experiment E7.
