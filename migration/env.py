import logging
from logging.config import fileConfig
import os
import re
import app.entities as entities
from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine, text

from alembic import context
load_dotenv()



# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")



# gather section names referring to different
# databases.  These are named "engine1", "engine2"
# in the sample .ini file.
# db_names = config.get_main_option("databases", "")

# add your model's MetaData objects here
# for 'autogenerate' support.  These must be set
# up to hold just those tables targeting a
# particular database. table.tometadata() may be
# helpful here in case a "copy" of
# a MetaData is needed.
# from myapp import mymodel
# target_metadata = {
#       'engine1':mymodel.metadata1,
#       'engine2':mymodel.metadata2
# }
target_metadata = None

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
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    url_tokens = {
        "DB_USER": os.getenv("POSTGRES_USER", ""),
        "DB_PASS": os.getenv("POSTGRES_PASSWORD", ""),
        "DB_HOST": os.getenv("POSTGRES_HOST", ""),
        "DB_NAME": os.getenv("POSTGRES_DB", ""),
    }
    url = config.get_main_option("sqlalchemy.url")
    url = re.sub(r"\${(.+?)}", lambda m: url_tokens[m.group(1)], url)  # type: ignore
    print("#############################################################")
    print(url)
    print("#############################################################")
    engine = create_engine(url)

    is_autogenerating:bool = True if config.cmd_opts and hasattr(config.cmd_opts,'autogenerate') and config.cmd_opts.autogenerate else False

    targeted_schema = context.get_x_argument(as_dictionary=True).get("tenant")

    def process_revision_directives(context, revision, directives):
        if is_autogenerating:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                print('No changes in schema detected.')

    translated = entities.Base.metadata
    with engine.connect() as connection:
        if not is_autogenerating :
            if targeted_schema:
                schemas = list[str](map(lambda row: row[0],connection.execute(text("SELECT schema FROM public.companies")).fetchall()))
                if targeted_schema in schemas:
                    translated = MetaData(schema=targeted_schema)
                else:
                    raise Exception("schema not found")
                #re assign the selected schema to the table
                print("#############################")
                print('updating schema:',translated.schema)
                print("#############################")

                connection.execute(text('CREATE SCHEMA IF NOT EXISTS "%s"' % translated.schema))
                connection.execute(text('set search_path to "%s"' % translated.schema))
                connection.dialect.default_schema_name = translated.schema
                connection.commit()

        context.configure(
            connection=connection,
            target_metadata=translated,
            compare_type=True,
            include_schemas= not is_autogenerating,
            process_revision_directives=process_revision_directives
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()