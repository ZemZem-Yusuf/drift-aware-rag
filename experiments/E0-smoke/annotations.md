# E0 annotations (human verdicts)

Generated data: [`results/20261107T100022Z-baseline.json`](results/20261107T100022Z-baseline.json)
(commit `7d0608f`, index `k8s-1.33-e5`, prompt `answer-v1`, `gemini-2.5-flash`, top_k 5).
Retrieval diagnosis: [`results/20261107T100116Z-diagnose-restart.json`](results/20261107T100116Z-diagnose-restart.json).

Verdicts by Youssef Zemzem, 2026-11-07, checked against the Kubernetes v1.33 documentation.

| Question | Verdict | Notes |
|---|---|---|
| `restart-deployment` | ❌ **Wrong answer** | Misses the canonical `kubectl rollout restart deployment/<name>` and suggests `kubectl patch`. Cause: **retrieval** (see diagnosis below), not generation: the right chunk never reached the prompt. |
| `probes` | ✅ Correct | Grounded, 4 relevant sources, explains both probes and how they relate. |
| `resource-limits` | ⚠️ Partly correct | Explains how limits are enforced (cgroups, throttling, OOM kill) but omits the basic `resources.limits` YAML example and writes `resource: limits.cpu` instead of `resources.limits.cpu`. |
| `pod-fr` | ✅ Correct | Answers in French from the French docs. |
| `out-of-scope` | ✅ Correctly refused | No invented answer. |

**Summary:** 3 correct (incl. the refusal), 1 partly correct, 1 wrong, out of 5. A qualitative smoke test, not a benchmark: too few questions for a percentage to mean anything.

## Diagnosis of the wrong answer

| Query | `kubectl_rollout_restart.md` vector rank | keyword rank | fused rank |
|---|---|---|---|
| "How do I restart all the pods of a Deployment?" | not in top 200 | 21 | **58** |
| "kubectl rollout restart deployment" | 1 | 1 | **1** |

The reference page is written in command vocabulary ("Restart a resource"); the user asks in task vocabulary ("restart all the pods"). The small embedding model doesn't bridge the two, and keyword search alone ranks it too low for fusion to recover.

## Follow-ups (to be measured on the golden set, not decided by intuition)
- Add `restart-deployment` and `resource-limits` to the golden set as known hard cases.
- Hypotheses to test: (H1) embed the heading path together with the chunk text; (H2) add a cross-encoder reranker over the top 50; (H3) rewrite the query before retrieval; (H4) tune the keyword/vector fusion weights.
