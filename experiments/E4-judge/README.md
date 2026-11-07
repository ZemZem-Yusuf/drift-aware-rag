# E4: answer quality, and can an LLM judge be trusted to measure it?

Retrieval is measured (R1); answers aren't yet. Phase 3 needs an **answer-drift detector**
(layer L4) that scores live traffic without a person reading every answer, which means an LLM
judge. A judge is only useful if it agrees with a careful human, so this experiment measures
that agreement *before* the judge is used for anything.

Two outputs:
1. **Answer-quality baseline** from human labels: share of answers fully supported by their
   sources, share that answer the question correctly, refusal behaviour, with 95% bootstrap
   intervals.
2. **Judge calibration:** agreement between LLM judges and the human labels (Cohen's κ with a
   bootstrap interval, confusion matrix, cost per judgement).

## Protocol (fixed before any answer was generated)

### Step 1: answers (`generate_answers.py`)
- Every verified golden item in `golden/k8s-1.33.jsonl`: 85 retrieval questions plus 4
  out-of-scope questions (which should be refused).
- The production pipeline as it stands: `active` index (version 2), hybrid retrieval with the
  default settings, **no reranker**, top 5 sources, prompt `answer-v1`, generator
  `gemini/gemini-2.5-flash`, temperature 0.
- The results file stores, per question, the answer, the 5 sources exactly as the model saw
  them, citations, refusal flag, tokens and latency. Answers are cached, so the run is
  reproducible without new provider calls.

### Step 2: human labels (`driftrag-label`), blind
The labeller sees the question, the reference answer, the system's answer and the full text of
the 5 sources. **No judge output exists while labelling**: judges are run only after all labels
are in, so they can't anchor the human.

| Answer type | Label | Definition |
|---|---|---|
| Answered | **supported** | yes = every statement in the answer is backed by the sources shown; no = at least one statement isn't (outside knowledge, wrong detail, or a contradiction) |
| Answered | **correct** | yes = it answers the question and agrees with the reference answer on what matters; no = wrong, incomplete on the main point, or answers something else |
| Refused, in-scope question | **refusal justified** | yes = the 5 sources really don't contain the answer (a retrieval miss, handled honestly); no = the answer was in the sources |
| Refused, out-of-scope question | none | correct by definition |

Supported and correct are independent: an answer can be faithful to the wrong sources
(supported, not correct) or right from outside knowledge (correct, not supported).

### Step 3: judges (separate PR, after labels)
- Judges: `gemini/gemini-2.5-flash` (same model as the generator: self-preference risk) and
  `gemini/gemini-2.5-flash-lite` (cheaper). Prompt `judge-v1`, written and committed before
  it is run; same inputs as the human; binary verdicts with a one-line reason.
- Agreement per label: Cohen's κ, 95% bootstrap interval over answers, confusion matrix.
- **Adoption rule (declared now):** a judge is used as an automatic gate for a label only if
  κ ≥ 0.6 and the lower end of its 95% interval is ≥ 0.4. Otherwise it may be shown on
  dashboards as an indicator but never blocks or triggers anything.

## Known limitations
- **One labeller.** κ here is judge-vs-one-person; no human-human agreement is measured.
- **About 80 labelled answers**, not the ~200 in the roadmap: κ intervals will be wide (roughly
  ±0.15). Enough to reject a bad judge, not to rank two good ones finely.
- Answers are mostly good or mostly bad by question type, so class imbalance can make κ low
  even when raw agreement is high; raw agreement is reported next to κ.

## Files
- `generate_answers.py`: step 1. `results/*-answers.json`: generated answers.
- `LABELS.md`: the current labelling sheet (`uv run driftrag-label sheet --max-items 15`).
- `sheets/`: every completed sheet, kept as evidence.
- `labels/human.jsonl`: the human labels (judgements, so kept apart from generated results).
