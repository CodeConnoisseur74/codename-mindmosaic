from logging.config import fileConfig

from alembic import context
from api.models import StudyPlan, User  # ✅ Keep these imports
from decouple import config  # ✅ Load env variables
from sqlalchemy import create_engine, pool
from sqlmodel import SQLModel

# ✅ Load DATABASE_URL from .env
DATABASE_URL = config('DATABASE_URL')

# ✅ Alembic Config object
config = context.config
config.set_main_option('sqlalchemy.url', DATABASE_URL)  # ✅ Inject DB URL dynamically

# ✅ Set up logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ✅ Define target metadata so Alembic detects schema
target_metadata = SQLModel.metadata

# ✅ Explicitly reference models to prevent "unused import" warnings
_ = StudyPlan, User  # 🔹 This tells the linter they are intentionally imported


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    context.configure(
        url=DATABASE_URL,  # ✅ Use dynamic DB URL
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = create_engine(
        DATABASE_URL, poolclass=pool.NullPool
    )  # ✅ Use create_engine

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
