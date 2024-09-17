import os
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import os
from app.utils.constants import INVALID_SCHEMA, MASTER_SCHEMA

load_dotenv()  # Load environment variables from .env file

SQL_USER = os.getenv("POSTGRES_USER")
SQL_PASSWORD = os.getenv("POSTGRES_PASSWORD")
SQL_HOST = os.getenv("POSTGRES_HOST")
SQL_DB = os.getenv("POSTGRES_DB")
SQLALCHEMY_DATABASE_URL = f"postgresql://{SQL_USER}:{SQL_PASSWORD}@{SQL_HOST}/{SQL_DB}"

db_connections:dict[str,dict[str,Session|datetime]] = {}

# Create a SQLAlchemy engine
engine = sa.create_engine(
    SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True, pool_recycle=280
)
# Create a base class for declarative models
Base = declarative_base(metadata=sa.MetaData())


class TenantNotFoundError(Exception):
    def __init__(self, id):
        self.message = "Tenant %s not found!" % str(id)
        super().__init__(self.message)


def only_master(db: Session):
    if db.connection().dialect.default_schema_name == MASTER_SCHEMA:
        return db
    else:
        raise Exception(INVALID_SCHEMA)

def get_master_database():
    return build_db_session(MASTER_SCHEMA)


def build_db_session(schema: str) -> Session:
    if schema:
        schema_translate_map = dict(tenant=schema)
    else:
        raise TenantNotFoundError("Tenant %s not found!" % schema)
    connectable = engine.execution_options(schema_translate_map=schema_translate_map)
    connectable.dialect.default_schema_name = schema
    db = sessionmaker(bind=connectable, expire_on_commit=False)()
    db.execute(sa.text('set search_path to "%s"' % schema))
    return db

def get_connected_schema(db:Session)->str:
    return db.connection().dialect.default_schema_name