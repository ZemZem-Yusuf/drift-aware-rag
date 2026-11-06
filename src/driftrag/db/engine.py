"""SQLAlchemy engine helpers."""

from sqlalchemy import Engine, create_engine

_DRIVER = "postgresql+psycopg://"


def sqlalchemy_url(dsn: str) -> str:
    """Turn a plain ``postgresql://`` DSN into a SQLAlchemy URL that uses the psycopg 3 driver."""
    for prefix in ("postgresql://", "postgres://"):
        if dsn.startswith(prefix):
            return _DRIVER + dsn.removeprefix(prefix)
    return dsn


def make_engine(dsn: str) -> Engine:
    return create_engine(sqlalchemy_url(dsn), pool_pre_ping=True)
