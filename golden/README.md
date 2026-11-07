# Golden set: Kubernetes docs v1.33

`k8s-1.33.jsonl`: questions with the documentation sections that answer them and a short
reference answer. Used to measure retrieval (recall@k, MRR, nDCG) and, later, answer quality.

## How it was built
1. **Drafted** by an LLM (Claude; `origin: llm-drafted`) from the real corpus: every relevant
   section was looked up in the ingested index, so each reference points to text that exists.
2. **LLM pre-review** by a second, independent model (ChatGPT, 2026-11-07), applying the rule
   "every claim in a reference answer must be supported by the referenced sections". Its notes
   were used to tighten 12 answers; for 15 others the claims were confirmed in the full section
   text. This pass was **not** checked by a person and verified nothing; it's kept as-is in
   [`reviews/`](reviews/) and summarised in each item's notes.
3. **Human review**, item by item, against the full documentation sections shown in
   [`REVIEW.md`](REVIEW.md) (`uv run driftrag-golden sheet` / `apply`). Only items marked
   `verified` (with the reviewer's name) count in reported numbers.

### v2 (2026-11-07): growing the set for statistical power
With 28 verified questions, only large effects could be detected (H2's +0.065 recall@5 wasn't
significant). v2 adds 57 drafts aimed at the gaps of v1: tasks (+25), troubleshooting (+12),
commands (+11) and French (+12). Each was drafted from sections looked up in the index, then
**self-checked** by the drafter: every command and field name in an answer was searched for in
the full referenced text, which caught and fixed 6 drafting errors (e.g. `kubectl exec -it`
where the docs use `--stdin --tty`). The self-check verifies nothing; the human review does.
Drafts are reviewed in batches (`driftrag-golden sheet --max-items 15`).

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
