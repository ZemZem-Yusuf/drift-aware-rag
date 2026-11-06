# ADR-0002: Statistical test for query drift (L1)

- **Status:** Proposed. The decision is made from experiment E1 data, not opinion.
- **Date:** 2026-11-07
- **Deciders:** Youssef Zemzem

## Context

Layer L1 watches *what users ask about*. Each query becomes an embedding (384–1024 dimensions). The detector compares a **reference window** (e.g. last month) with a **current window** (e.g. today) and must answer: "do these two samples come from the same distribution?"

Requirements:

1. Works on high-dimensional embeddings, not just one number.
2. Detects **multi-modal** shifts: a new topic cluster appearing while the average barely moves.
3. Has a **controllable false-alarm rate**. Too many alarms and people ignore them; every alarm can trigger costly remediation.
4. Works with small windows (50–500 queries), because low-traffic systems must be monitored too.
5. Cheap enough to run daily on CPU.

## Options considered

| Option | How it works | Strengths | Weaknesses |
|---|---|---|---|
| A. **Centroid cosine distance** (the build guide's suggestion) | Distance between the mean embeddings of the two windows | Trivial, fast; the baseline | Misses shifts that don't move the mean (a new cluster balanced by a shrinking one); no p-value, so thresholds are hand-picked |
| B. **Per-dimension KS tests** + multiple-testing correction | Kolmogorov–Smirnov test on each dimension, then Bonferroni/FDR | Familiar, exact p-values | Ignores correlations between dimensions; hundreds of tests lose power after correction |
| C. **MMD** (maximum mean discrepancy) with a **permutation test** | Kernel distance between the two samples; the p-value comes from reshuffling the window labels | Captures any difference in distribution, including multi-modal ones; principled p-value | O(n²) kernel cost (fine at ≤ 2k points); the kernel bandwidth must be chosen (median heuristic) |
| D. **Classifier two-sample test (C2ST)** | Train a classifier to tell the windows apart; AUC ≈ 0.5 means no drift | Powerful; the classifier shows *which* queries are new | Needs more data to be reliable; training cost per check; can overfit on small windows |
| E. **Cluster PSI** | Cluster the reference (k-means), compare the share of queries per cluster with the population stability index | Interpretable ("cluster 7 grew from 2% to 15%"); industry-standard PSI thresholds | Depends on k and the clustering; blind to changes inside a cluster |
| F. **Evidently** (library) | Wraps several tests for embeddings | Widely used; a good external baseline | Less control over calibration; we still need our own threshold logic |

## Evaluation plan (experiment E1)

- Inject a topic shift of 0%, 5%, 10%, 20% and 50% into synthetic traffic, with windows of 50, 200, 500 and 2,000 queries, 5 seeds each.
- For each detector, set the threshold for **≤ 1 false alarm per 30 daily checks**, estimated by bootstrapping the reference window.
- Measure **power** (detection rate) per shift size and window size, **detection delay**, and CPU time.
- Results go to `experiments/E1/results/` and `docs/results.md`.

## Decision

> _To be written by the author after E1 (what was chosen, why, and what was rejected)._
>
> Working hypothesis to test: MMD (C) as the primary alarm, with cluster PSI (E) as the explanation shown to humans, and centroid distance (A) kept only as a baseline in the results table.

## Consequences

> _To be written with the decision._

## When to revisit

- Traffic grows so windows exceed ~5k queries → MMD cost; consider linear-time MMD or C2ST.
- The embedding model changes → see experiment E3: the reference window must be re-embedded with the new model, or every check will raise a false alarm.
