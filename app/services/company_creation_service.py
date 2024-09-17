from dataclasses import dataclass
import traceback
import uuid
from fastapi import Depends
from sqlalchemy.orm import Session
import sqlalchemy as sa
from alembic import command, script
from alembic.config import Config
from alembic.migration import MigrationContext
from app.connectors.database_connector import get_master_database
from app.entities.company import Company
from app.utils.constants import DB_NOT_UPTODATE
from app.utils.project_dependencies import master_database
from app.utils.utils import get_project_root, get_randome_str
import argparse

@dataclass
class CompanyCreationService:

    db: Session = Depends(master_database)

    @staticmethod
    def __get_current_head(db: Session):
        connection = db.connection()
        context = MigrationContext.configure(connection)
        current_head = context.get_current_revision()
        if current_head == None:
            raise Exception(DB_NOT_UPTODATE)
        return current_head

    @staticmethod
    def __upgrade(schema: str, current_head: str):
        alembic_config = Config(get_project_root().joinpath("alembic.ini"))
        alembic_script = script.ScriptDirectory.from_config(alembic_config)
        config_head = alembic_script.get_current_head()
        if current_head != config_head:
            raise RuntimeError(
                "Database is not up-to-date. Execute migrations before adding new tenants."
            )
        # If it is required to pass -x parameters to alembic
        x_arg = "".join(["tenant=", schema])  # "dry_run=" + "True"
        alembic_config.cmd_opts = argparse.Namespace()  # arguments stub
        if not hasattr(alembic_config.cmd_opts, "x"):
            if x_arg is not None:
                setattr(alembic_config.cmd_opts, "x", [x_arg])
            else:
                setattr(alembic_config.cmd_opts, "x", None)
        command.upgrade(alembic_config, "head")

    @staticmethod
    def upgrade_all():
        db = get_master_database()
        try:
            current_head = CompanyCreationService.__get_current_head(db)
            for company in db.query(Company).all():
                CompanyCreationService.__upgrade(company.schema, current_head)
            db.commit()
            db.flush()
        except:
            db.rollback()
            traceback.print_exc()
        finally:
            db.close()

    def create_company(self, name: str) -> Company:
        schema = get_randome_str()
        tenant = Company()
        tenant.name = name
        tenant.logo_path = "none"
        tenant.schema = schema
        tenant.access_key = uuid.uuid4().hex
        self.db.execute(sa.schema.CreateSchema(schema, True))
        self.db.add(tenant)
        self.db.commit()
        current_head = CompanyCreationService.__get_current_head(self.db)
        CompanyCreationService.__upgrade(schema, current_head)
        return tenant

    def get_company(self, id: int) -> Company:
        return self.db.query(Company).filter(Company.id == id).first()  # type: ignore
