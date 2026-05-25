from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    work_email: EmailStr
    username: str
    title: Optional[str] = None
    department: Optional[str] = None

class UserCreate(UserBase):
    password: str
    role_name: str

class UserOut(UserBase):
    id: int
    org_id: int
    role_id: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "access"


    
# class UserInToken(BaseModel):
#     id: int
#     email: EmailStr
#     is_active: bool
