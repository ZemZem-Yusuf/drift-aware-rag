import uuid
from pathlib import Path

import pytest
from sqlalchemy import Engine

from driftrag.db.registry import set_alias
from driftrag.rag.chunking import ChunkerConfig
from driftrag.rag.corpus import read_snapshot
from driftrag.rag.embeddings import HashingEmbedder
from driftrag.rag.ingest import IngestReport, ingest
from driftrag.rag.retrieval import HybridRetriever, RetrievalError
from tests.snapshots import write_snapshot

pytestmark = pytest.mark.integration

EN_DOCS = {
    "deployments.md": """---
title: Deployments
---
A Deployment manages a set of Pods to run an application workload.

## Restarting a Deployment

Run kubectl rollout restart deployment/my-app to restart every Pod of the Deployment.
""",
    "services.md": """---
title: Service
---
A Service exposes an application running on a set of Pods as a network service.
""",
    "configmaps.md": """---
title: ConfigMaps
---
A ConfigMap stores non-confidential configuration data as key-value pairs.
""",
}

FR_DOCS = {
    "deployments.md": """---
title: Déploiements
---
Pour redémarrer les conteneurs d'un déploiement, utilisez kubectl rollout restart.
""",
}

EMBEDDER = HashingEmbedder(dim=256)


@pytest.fixture(scope="module")
def indexed(engine: Engine, tmp_path_factory: pytest.TempPathFactory) -> IngestReport:
    root: Path = tmp_path_factory.mktemp("corpus")
    version = uuid.uuid4().hex[:6]
    en = write_snapshot(root, EN_DOCS, version=version)
    fr = write_snapshot(root, FR_DOCS, version=version, lang="fr")
    with engine.begin() as conn:
        return ingest(
            conn,
            [*read_snapshot(en), *read_snapshot(fr)],
            index_name=f"retrieval-{version}",
            embedder=EMBEDDER,
            config=ChunkerConfig(min_chars=0),
        )


@pytest.fixture
def retriever(engine: Engine, indexed: IngestReport) -> HybridRetriever:
    # The alias is shared by all integration tests, so point it at our version right before use.
    with engine.begin() as conn:
        set_alias(conn, "active", indexed.version.id, reason="retrieval test")
    return HybridRetriever(engine, EMBEDDER)


def test_best_chunk_is_found_by_both_retrievers(retriever: HybridRetriever) -> None:
    # A query both searches agree on. (With a vaguer question, the word-matching test embedder
    # and keyword search can each put a different chunk first; RRF then gives both the same
    # score and the tie-break by id decides, which is correct but makes a poor test.)
    result = retriever.search("kubectl rollout restart deployment")
    best = result.chunks[0]
    assert best.heading_path == "Deployments > Restarting a Deployment"
    assert best.document_path == "deployments.md"
    assert (best.vector_rank, best.keyword_rank) == (1, 1)
    scores = [c.score for c in result.chunks]
    assert scores == sorted(scores, reverse=True)


def test_top_k_limits_results(retriever: HybridRetriever) -> None:
    assert len(retriever.search("pods", top_k=2).chunks) == 2


def test_language_filter_and_french_stemming(retriever: HybridRetriever) -> None:
    result = retriever.search("redémarrer les conteneurs", lang="fr")
    assert result.chunks
    assert {c.lang for c in result.chunks} == {"fr"}
    assert result.chunks[0].keyword_rank == 1  # 'conteneurs' matched via French stemming


def test_keyword_only_match_is_reported(retriever: HybridRetriever) -> None:
    result = retriever.search("ConfigMap key-value")
    configmap = next(c for c in result.chunks if c.document_path == "configmaps.md")
    assert configmap.keyword_rank == 1


def test_keyword_search_matches_partial_questions(retriever: HybridRetriever) -> None:
    # 'expose' and 'network' appear only in the Service doc; 'kubernetes' appears nowhere.
    result = retriever.search("which kubernetes object can expose an app on the network")
    service = next(c for c in result.chunks if c.document_path == "services.md")
    assert service.keyword_rank == 1


def test_query_words_are_stemmed_only_once(retriever: HybridRetriever) -> None:
    # 'exposes' stems to 'expos'; stemming that again would give 'expo' and match nothing.
    result = retriever.search("exposes")
    assert result.chunks[0].document_path == "services.md"
    assert result.chunks[0].keyword_rank == 1


def test_wrong_embedding_model_is_refused(engine: Engine, retriever: HybridRetriever) -> None:
    other = HybridRetriever(engine, HashingEmbedder(dim=64))
    with pytest.raises(RetrievalError, match="can't be compared"):
        other.search("pods")
