from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from app.routes.route_entries import PROTECTED_ROUTES, PUBLIC_ROUTES
from app.utils.auth_dependencies import verify_auth_token
security = HTTPBearer()


def setup_routes(app: FastAPI):
    for route in PUBLIC_ROUTES:
        app.include_router(route)

    for route in PROTECTED_ROUTES:
        dependcies = [Depends(security), Depends(verify_auth_token)]
        app.include_router(route, dependencies=dependcies)