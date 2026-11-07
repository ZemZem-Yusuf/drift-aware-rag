"""H6 follow-up: do inlined code samples change the *answers* to configuration questions?

R1 measures retrieval only. H6 barely moved retrieval, so this checks the other half: for a
few "how do I configure" questions, generate answers from the baseline index (``active``) and
from the code-samples index (``canary``) and record whether the answer contains the exact
field names a correct manifest needs.

    uv run python experiments/R1-retrieval/h6_answers.py
"""

from __future__ import annotations

from pathlib import Path

from driftrag.config import get_settings
from driftrag.db.engine import make_engine
from driftrag.experiments.records import environment, save_run
from driftrag.llm.factory import build_llm_client
from driftrag.rag.embeddings import E5Embedder
from driftrag.rag.generation import AnswerGenerator
from driftrag.rag.retrieval import HybridRetriever

REPO = Path(__file__).resolve().parents[2]
QUESTIONS = {
    "configmap-env": (
        "How can I turn every key of a ConfigMap into environment variables in my container?",
        ["envFrom", "configMapRef"],
    ),
    "pdb-keep-replicas": (
        "How do I make sure at least two replicas stay up while nodes are being drained?",
        ["PodDisruptionBudget", "minAvailable"],
    ),
    "netpol-default-deny": (
        "How do I block all incoming traffic to the pods in a namespace by default?",
        ["NetworkPolicy", "podSelector", "policyTypes"],
    ),
}


def main() -> None:
    settings = get_settings()
    engine = make_engine(settings.database_url.get_secret_value())
    embedder = E5Embedder()
    llm = build_llm_client(settings)
    results = {}
    for alias in ("active", "canary"):
        generator = AnswerGenerator(
            HybridRetriever(engine, embedder, alias=alias), llm, model=settings.generator_model
        )
        for qid, (question, fields) in QUESTIONS.items():
            answer = generator.answer(question)
            present = [f for f in fields if f in answer.text]
            results.setdefault(qid, {})[alias] = {
                "index_version": answer.index_version.name if answer.index_version else None,
                "answer": answer.text,
                "refused": answer.refused,
                "expected_fields": fields,
                "fields_present": present,
                "citations": [c.document_path for c in answer.citations],
            }
            print(f"{qid} [{alias}]: {len(present)}/{len(fields)} fields {present}")
    path = save_run(
        REPO / "experiments",
        "R1-retrieval",
        "h6-answers",
        environment=environment(REPO, settings),
        config={"aliases": ["active", "canary"], "top_k": 5},
        results=results,
    )
    print(f"saved {path.relative_to(REPO)}")


if __name__ == "__main__":
    main()
