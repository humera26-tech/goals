from pydantic import BaseModel, EmailStr
from datetime import date 
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


class UserBasicOut(BaseModel):
    id: int
    username: str
    work_email: EmailStr
    title: Optional[str]
    department: Optional[str]
    # org_id: int
    role_id: int
    
    model_config = {
        "from_attributes": True
    }

class UserCreateInOrg(BaseModel):
    work_email: EmailStr
    username: str
    password: str
    title: Optional[str] = None
    department: Optional[str] = None
    role_name: Optional[str] = "Member" #temporory

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str

# schema for user_details
class UserDetailsBase(BaseModel):
    personal_email: Optional[EmailStr] = None
    dob: Optional[date] = None
    pwd_flag: Optional[bool] = None
    maritalstatus_flag: Optional[bool] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None


class UserDetailsCreate(UserDetailsBase):
    pass

class UserDetailsUpdate(BaseModel):
    # all optional
    personal_email: Optional[EmailStr] = None
    dob: Optional[date] = None
    pwd_flag: Optional[bool] = None
    maritalstatus_flag: Optional[bool] = None
    gender: Optional[str] = None
    nationality: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None


class UserDetailsOut(UserDetailsBase):
    user_id: int
    model_config = {
        "from_attributes": True
    }
