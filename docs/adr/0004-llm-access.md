# ADR-0004: How the system calls LLMs and embedding models

- **Status:** Proposed
- **Date:** 2026-11-07
- **Deciders:** Youssef Zemzem

## Context

The system needs three kinds of model calls:

1. **Embeddings** for every chunk (tens of thousands, re-run on every re-index) and every query.
2. **Generation** of answers with citations.
3. **Judging** answers (faithfulness, relevance) for the eval gate and online monitoring.

Constraints:
- Budget is zero: only free tiers and the laptop's CPU.
- Free tiers have daily caps that change without notice, and providers may use free-tier prompts for training, so **only public data** may be sent.
- Results must be **reproducible**: rerunning an experiment must give the same numbers.
- **CI must never call a real API** (no keys in CI, no rate limits, deterministic tests).
- The judge should come from a **different model family** than the generator, to avoid self-preference bias.
- Upstream model drift (layer L6) is part of the project, so the model version must be recorded on every call.

## Options considered

### Calling LLMs

| Option | Strengths | Weaknesses |
|---|---|---|
| A. **Provider SDKs directly** (google-genai, groq, …) | No extra layer | One client per provider; retries, fallbacks, cost tracking written by hand |
| B. **LiteLLM SDK** behind our own small `LLMClient` interface | One API over 100+ providers; retries, fallbacks and cost tracking built in; widely used | Another dependency; its abstractions sometimes lag new provider features |
| C. **LangChain chat models** | Familiar | Pulls in a large framework for a thin need; harder to keep the pipeline plain and testable |

### Embeddings

| Option | Strengths | Weaknesses |
|---|---|---|
| D. **Local small model** (BGE/E5-small class) via sentence-transformers on CPU | Free, no rate limits, fully reproducible, data never leaves the machine | Lower quality than large hosted models; ~1 GB of dependencies (PyTorch CPU) in the project venv |
| E. **Hosted embedding API** (Gemini, OpenAI) | Higher quality | Rate limits on re-indexing; costs; results can change if the provider updates the model |

### Determinism

| Option | Notes |
|---|---|
| G. **Response cache** keyed by (model, prompt hash, parameters) | Reruns are free and identical |
| H. **Recorded responses** for tests + a **fake provider** | CI runs without keys or network |

## Decision

> _To be written by the author._
>
> Proposed: B for LLMs, behind a small interface so tests can swap in a fake provider; D for embeddings, with the model name and version stored on every chunk and query; G and H for determinism. Generator: a Gemini Flash-class model; judge: a different family (e.g. via Groq). Fallback provider on rate-limit errors.

## Consequences

> _To be written with the decision._ Points to cover: what's lost with a small local embedding model (and how E3 measures the effect of switching), and what happens when a free tier disappears.

## When to revisit

- Retrieval quality is limited by the embedding model (measured on the golden set) → compare a larger local model and a hosted one.
- A free tier is removed → switch provider in configuration; the interface makes this a config change.
