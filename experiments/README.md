# Experiments

Every number this project reports comes from a run saved here, which anyone can reproduce.

## Layout

```
experiments/<ID>-<name>/
  run.py            the script that produces the results (committed before it is run)
  results/*.json    generated runs, one file per run, never edited by hand
  annotations.md    human judgements on the runs, dated and signed
```

Each results file contains:

| Field | What it records |
|---|---|
| `environment.git` | commit hash, and `dirty: true` if the working tree had uncommitted changes |
| `environment.packages`, `python`, `platform` | software versions |
| `environment.settings` | models and limits (secrets are never recorded) |
| `environment.index` | index version, embedding model, chunker config and chunk counts |
| `config` | parameters of this run |
| `results` | raw outputs and measurements |

## Rules

1. **Commit the script, then run it.** A run must point to a clean commit (`dirty: false`).
2. **Never edit a results file.** Wrong run? Fix the script and run again; keep both files.
3. **Judgements go in `annotations.md`,** separate from generated data, with a date and a name.
4. **LLM answers are cached** (by model, prompt and parameters), so rerunning a script reproduces the same answers without spending quota.
5. **Negative results are kept.** A hypothesis that didn't help is still a result.

## Index

| ID | Question | Status |
|---|---|---|
| [E0](E0-smoke/) | Does the full pipeline work end to end on the real corpus? | Done 2026-11-07: works; 1 retrieval failure diagnosed |
| [R1](R1-retrieval/) | How good is retrieval on the human-verified golden set? | Baseline 2026-11-07: recall@5 0.607 [0.446, 0.762], n=28 |
| [R1/H6](R1-retrieval/) | Do inlined code samples improve retrieval? | 2026-11-07: no (recall@5 Δ 0.000; MRR Δ +0.040 [−0.007, +0.097]); small answer gain on config questions |
| [R1/H1](R1-retrieval/) | Does embedding section titles with the text improve retrieval? | 2026-11-07: no, rejected (recall@5 -0.024 [-0.107, +0.036]); headings pushed some relevant pages down |
| [R1/H4](R1-retrieval/) | Do fusion weights or candidate depth improve retrieval? | 2026-11-07: no, rejected (pre-declared grid of 8; best recall@5 diff 0.000; keyword-heavy -0.089) |
| E1 | Which detector best catches query drift at a fixed false-alarm rate? | Planned |
| E2 | Which remediation recovers quality fastest and cheapest? | Planned |
| E3 | Does changing the embedding model cause false drift alarms? | Planned |
| E4 | Can the LLM judge be trusted as an eval gate (agreement with human labels)? | Planned |
| E5 | Does the probe set catch a silent upstream model change? | Planned |
| E6 | How much traffic must be judged to detect answer drift? | Planned |
