"""Alembic environment. The database URL comes from the Alembic config if set (tests),
otherwise from ``DRIFTRAG_DATABASE_URL`` via the application settings."""

from alembic import context
from sqlalchemy import create_engine, pool

from driftrag.db.engine import sqlalchemy_url

config = context.config


def _url() -> str:
    configured = config.get_main_option("sqlalchemy.url")
    if configured:
        return configured
    from driftrag.config import get_settings

    return sqlalchemy_url(get_settings().database_url.get_secret_value())


def run_migrations_offline() -> None:
    context.configure(url=_url(), literal_binds=True, dialect_opts={"paramstyle": "named"})
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
