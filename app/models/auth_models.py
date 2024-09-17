
from pydantic import (
    BaseModel, 
    EmailStr
)


class LoginRequest(BaseModel):
    userName: EmailStr
    password: str

class LoginResponse(BaseModel):
    id: int
    name: str
    role: str
    contact: str
    access_token: str