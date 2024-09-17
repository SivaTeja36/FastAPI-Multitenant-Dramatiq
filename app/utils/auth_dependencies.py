import os
from dotenv import load_dotenv
from fastapi import Request
from app.models.user_models import CurrentContextUser
from jose import jwt

from app.utils.constants import AUTHORIZATION

load_dotenv()

SECRET_KEY: str = os.getenv("JWT_SECRET")  # type: ignore
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300  # 3 hours


def __verify_jwt(token: str):
    token = token.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_sub": True})  # type: ignore
    user = payload.get("sub")
    if user:
        cur_user = CurrentContextUser()
        cur_user.username = str(user)
        return cur_user


async def verify_auth_token(request: Request):
    if (
        "login" not in request.url.path
        and "refresh" not in request.url.path
        and "admin" in request.url.path
    ):
        auth: str = request.headers.get(AUTHORIZATION) or ""
        try:
            token = auth.strip().rsplit(".", 1)[0]
            request.state.user = __verify_jwt(token=token)
        except Exception:
            request.state.user = __verify_jwt(token=auth)
