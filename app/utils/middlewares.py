import traceback
from fastapi import FastAPI, Request
from jose import JOSEError
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.connectors.database_connector import (
    TenantNotFoundError,
    build_db_session,
    get_master_database
)
from app.entities.company import Company
from app.routes.route_entries import PROTECTED_ROUTES
from app.utils.constants import AUTHORIZATION
from fastapi import status
from fastapi import HTTPException
from fastapi.responses import JSONResponse


class CreateTenentDbMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request, call_next):
        response=""
        try:
            self.__add_db_to_request(request)
            response = await call_next(request)
            if hasattr(request.state, "db"):
                request.state.db.commit()
        except HTTPException as e:
            response = self.__build_error_response(
                request, e.detail, status_code=e.status_code
            )
        except JOSEError as e:
            response = self.__build_error_response(
                request,
                content="\n".join([str(arg) for arg in e.args]),
                status_code=status.HTTP_401_UNAUTHORIZED,
            )
        except ValidationError as e:
            response = self.__build_error_response(
                request,
                e.__str__(),
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            response = self.__build_error_response(
                request,
                "\n".join([str(arg) for arg in e.args]),
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        finally:
            try:
                if hasattr(request.state, "db"):
                    request.state.db.close()
            except:
                traceback.print_exc()
        response.headers.update({"Server": ""})
        return response

    def __add_db_to_request(self, request: Request):
        tenent_routes = [route.prefix or "" for route in PROTECTED_ROUTES]
        if (
            any(prefix in request.url.path for prefix in tenent_routes)
            and "admin" not in request.url.path
        ):
            toekn = request.headers.get(AUTHORIZATION) or ""
            access_key = toekn.replace("Bearer ","").split(".").pop()
            master_db = get_master_database()
            company:Company = (
                    master_db.query(Company)
                    .where(Company.access_key == access_key)
                    .first()
                )
            if company:
                request.state.db = build_db_session(company.schema)
            else:
                raise TenantNotFoundError(access_key)
        else:
                request.state.db = get_master_database()

    def __build_error_response(self, request: Request, content: str, status_code):
        traceback.print_exc()
        if hasattr(request.state, "db"):
            request.state.db.rollback()
        return JSONResponse(
            content={
                "message": content.replace("\n", ": ").strip(),
                "url": str(request.url),
            },
            status_code=status_code,
            media_type="application/json",
        )



def setup_middlewares(app: FastAPI):
    # CORS middleware we are allowing api end points from any portal. because this api can be used with any portal as well as servers
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )
    app.add_middleware(CreateTenentDbMiddleware)
