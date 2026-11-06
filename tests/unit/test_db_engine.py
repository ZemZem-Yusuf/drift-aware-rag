import pytest

from driftrag.db.engine import sqlalchemy_url
from driftrag.db.registry import IndexVersion


@pytest.mark.parametrize(
    ("dsn", "expected"),
    [
        ("postgresql://u:p@h:5433/db", "postgresql+psycopg://u:p@h:5433/db"),
        ("postgres://u:p@h/db", "postgresql+psycopg://u:p@h/db"),
        ("postgresql+psycopg://u:p@h/db", "postgresql+psycopg://u:p@h/db"),
    ],
)
def test_sqlalchemy_url_uses_psycopg3(dsn: str, expected: str) -> None:
    assert sqlalchemy_url(dsn) == expected


def test_partition_name_is_built_from_an_integer_id() -> None:
    version = IndexVersion(id=7, name="x", embedding_model="m", embedding_dim=3, status="ready")
    assert version.partition == "rag.chunks_v7"
