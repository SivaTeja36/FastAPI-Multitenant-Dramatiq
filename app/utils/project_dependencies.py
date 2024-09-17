from fastapi import Request
from app.connectors.database_connector import only_master


def company_database(request: Request):
    return request.state.db

def master_database(request: Request):
    return only_master(request.state.db)