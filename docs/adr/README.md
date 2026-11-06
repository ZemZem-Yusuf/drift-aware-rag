# Architecture Decision Records

Each ADR records one significant decision: the context, the options considered, what was chosen and why, and when to revisit it. ADRs are never edited after acceptance; a new ADR supersedes an old one.

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-postgres-pgvector.md) | PostgreSQL + pgvector as the single data store | Accepted |
| [0002](0002-query-drift-detector.md) | Statistical test for query drift (L1) | Proposed (pending experiment E1) |
| [0003](0003-remediate-before-retraining.md) | Fix drift by remediation, not retraining | Proposed |
| [0004](0004-llm-access.md) | How the system calls LLMs and embedding models | Proposed |

Template: Status · Date · Deciders → Context → Options considered → Decision → Consequences → When to revisit.
