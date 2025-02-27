from logging.config import fileConfig

from alembic import context
from api.models import StudyPlan, User  # ✅ Keep these imports
from sqlalchemy import engine_from_config, pool

# ✅ Import SQLModel and models for Alembic to detect schema changes
from sqlmodel import SQLModel

# ✅ Suppress "imported but unused" warning by referencing models
_ = StudyPlan, User  # Prevents IDE and linter warnings

# Alembic Config object
config = context.config

# Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Define target metadata so Alembic detects schema
target_metadata = SQLModel.metadata  # ✅ This is necessary for autogenerate


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,  # ✅ Now it’s properly defined
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )  # ✅ Now it’s properly defined

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
