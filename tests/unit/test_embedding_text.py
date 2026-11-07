from driftrag.rag.chunking import Chunk
from driftrag.rag.ingest import embedding_text

CHUNK = Chunk(ordinal=0, heading_path="Taints and Tolerations > Concepts", content="A taint...")


def test_heading_goes_first_when_enabled() -> None:
    assert embedding_text(CHUNK, with_heading=True) == (
        "Taints and Tolerations > Concepts\n\nA taint..."
    )


def test_content_only_by_default_behaviour() -> None:
    assert embedding_text(CHUNK, with_heading=False) == "A taint..."


def test_empty_heading_adds_nothing() -> None:
    chunk = Chunk(ordinal=0, heading_path="", content="text")
    assert embedding_text(chunk, with_heading=True) == "text"
