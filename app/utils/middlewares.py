import traceback
from fastapi import (
    FastAPI, 
    Request,
    status,
    HTTPException
)
from fastapi.responses import (
    JSONResponse, 
    Response
)
from jose import JOSEError
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


class CORSMiddlewareLocal(BaseHTTPMiddleware):
    def allow_cors(self, response: Response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "*"
        return response

    async def dispatch(self, request, call_next):
        if request.method == "OPTIONS":
            response = Response()
            self.allow_cors(response)
            return response
        response = await call_next(request)
        return self.allow_cors(response)


class GlobalErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = ""
        try:
            response = await call_next(request)
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
        return response

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
        allow_credentials=True,
        allow_methods=["*"],  # ["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],  # ["Origin", "Content-Type","Authorization"],
        expose_headers=["*"],
    )
    app.add_middleware(GlobalErrorHandlerMiddleware)
    app.add_middleware(CORSMiddlewareLocal)
