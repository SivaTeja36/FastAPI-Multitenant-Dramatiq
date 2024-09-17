
from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    userName: EmailStr
    password: str

class LoginResponse(BaseModel):
    access_token: str
    name:str
    role:str
    id:int
    contact:str