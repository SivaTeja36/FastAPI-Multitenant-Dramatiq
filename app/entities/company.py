from app.connectors.database_connector import Base
import sqlalchemy as sa
from datetime import datetime


class Company(Base):
    __tablename__ = "companies"

    id: int = sa.Column(sa.Integer, primary_key=True, nullable=False) 
    name: str = sa.Column(sa.String(256), nullable=False) 
    schema: str = sa.Column(sa.String(256), nullable=False) 
    logo_path: str = sa.Column(sa.String(500), nullable=True) 
    access_key: str = sa.Column(sa.String(500), nullable=True) 
    created_at: datetime = sa.Column(sa.DateTime, nullable=False, default=sa.func.now()) 
    is_active: bool = sa.Column(sa.Boolean, nullable=False, default=True) 
