import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.db.base import Base  # Import models' declarative base
from app import models         # Import models so Alembic can auto-generate migrations

from dotenv import load_dotenv

load_dotenv()

# Alembic Config object
config = context.config

# Interpret config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add models' metadata for 'autogenerate' support
target_metadata = Base.metadata

# Fetch DB URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://user:password@localhost/dbname")
config.set_main_option("sqlalchemy.url", DATABASE_URL)


def run_migrations_offline():
    
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,  # detect column type changes
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

