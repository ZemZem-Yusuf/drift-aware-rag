# Golden set: Kubernetes docs v1.33

`k8s-1.33.jsonl`: questions with the documentation sections that answer them and a short
reference answer. Used to measure retrieval (recall@k, MRR, nDCG) and, later, answer quality.

## How it was built
1. **Drafted** by an LLM (`origin: llm-drafted`) from the real corpus: every relevant section
   was looked up in the ingested index, so each reference points to text that exists.
2. **Reviewed by a person**, item by item, against the documentation excerpts shown in
   [`REVIEW.md`](REVIEW.md) (`uv run driftrag-golden sheet` / `apply`). Only items marked
   `verified` (with the reviewer's name) count in reported numbers.

## Design choices
- **Relevance per document + section, not per chunk.** Chunk ids change on every re-chunking or
  re-index; section paths don't. The golden set has to survive the re-indexing this project
  is about.
- **Questions in user language, not documentation language.** Copying the docs' wording would
  make retrieval look better than it is. Known hard cases (vocabulary gaps such as "restart all
  pods" vs `kubectl rollout restart`) are included on purpose.
- **Mix:** concepts, tasks, commands and troubleshooting; English and French; plus
  out-of-scope questions that the system must refuse (scored separately).

## Known limitations
- 30 retrieval questions is small: report every metric with its bootstrap interval, and don't
  read small differences as improvements.
- Drafting by an LLM can bias the questions towards what the model finds easy to phrase. The
  human review and the deliberate hard cases reduce, not remove, that bias. Questions from real
  users (forums, issue trackers) would be a useful addition.
- Relevance lists may miss other sections that also answer a question; recall can therefore be
  slightly underestimated. Reviewers can add sections during review.
