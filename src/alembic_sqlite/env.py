import os
from logging.config import fileConfig

from alembic import context

from core.environment_settings import get_environment_settings
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from data.database.models.base import Base

# Init settings for database url
dot_env_file = os.getenv("ENV_FILE", ".env")
SETTINGS = get_environment_settings(dot_env_file=dot_env_file)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = [Base.metadata]

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = SQLAlchemyDBManager.generate_sqlalchemy_url(
        SETTINGS.database_url,
        database_user=SETTINGS.database_user,
        database_password=SETTINGS.database_password,
    ).__str__()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    connectable = SQLAlchemyDBManager.create_sqlalchemy_engine_for_alembic(
        SETTINGS.database_url,
        SETTINGS.database_user,
        SETTINGS.database_password,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
