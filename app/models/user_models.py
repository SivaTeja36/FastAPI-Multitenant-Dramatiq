from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreationRequest(BaseModel):
    name:str
    username: EmailStr
    password:str
    role:str
    contact:str

class UserCreationResponse(BaseModel):
    id:int
    name:str 
    username:str 
    contact:str
    role:str
    created_at:datetime
    is_active:bool
    
class CurrentContextUser():
    username: str
    name:str
    role:str