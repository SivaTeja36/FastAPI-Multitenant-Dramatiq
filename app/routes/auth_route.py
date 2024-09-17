from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from app.models.auth_models import LoginRequest, LoginResponse
from jose import jwt
from app.services.user_service import UserService

from app.utils.auth_dependencies import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
)
from app.utils.constants import USER_NOT_FOUND
from app.utils.project_dependencies import company_database

router = APIRouter(tags=["Authentication"])


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    request: LoginRequest,
    service:UserService = Depends(UserService)
) -> LoginResponse:
    user = service.validate_user(request.userName, request.password)
    if user and user.verify_password(request.password):
        claims = {
            "sub": str(user.username),
            "role": user.role,
            "name": user.name,
            "contact": user.contact,
            "userid": user.id,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        }
        try:
            token = jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)
            return LoginResponse(
                access_token=token,
                name=user.name,
                role=user.role,
                contact=user.contact,
                id=user.id,
            )
        except Exception as e:
            print(e)
            raise e
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=USER_NOT_FOUND)
