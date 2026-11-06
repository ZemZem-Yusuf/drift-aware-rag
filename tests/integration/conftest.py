"""Integration fixtures: a real Postgres + pgvector in Docker (testcontainers).

Skipped automatically when Docker isn't available (e.g. on a laptop with Docker stopped);
CI always runs them.
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine, create_engine

ROOT = Path(__file__).resolve().parents[2]
IMAGE = "pgvector/pgvector:pg16"


def _docker_available() -> bool:
    try:
        import docker

        docker.from_env().ping()
    except Exception:
        return False
    return True


def _alembic_config(url: str) -> Config:
    config = Config(str(ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(ROOT / "migrations"))
    config.set_main_option("sqlalchemy.url", url)
    return config


@pytest.fixture(scope="session")
def pg_url() -> Iterator[str]:
    if not _docker_available():
        pytest.skip("Docker is not available")
    from testcontainers.postgres import PostgresContainer

    with PostgresContainer(IMAGE, driver="psycopg") as container:
        url = container.get_connection_url()
        config = _alembic_config(url)
        # Round-trip proves the downgrade works too.
        command.upgrade(config, "head")
        command.downgrade(config, "base")
        command.upgrade(config, "head")
        yield url


@pytest.fixture(scope="session")
def engine(pg_url: str) -> Iterator[Engine]:
    eng = create_engine(pg_url)
    yield eng
    eng.dispose()
