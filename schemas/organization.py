from pydantic import BaseModel, EmailStr
from typing import Optional
from schemas.auth import UserCreate, UserOut
from schemas.role import RoleOut


class OrganizationBase(BaseModel):
    org_prefix: str
    name: str
    email: EmailStr
    phone: Optional[str] = None
    logo_url: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[int] = None
    website: Optional[str] = None
    description: Optional[str] = None

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationOut(OrganizationBase):
    id: int
    
class OrgWithUserCreate(BaseModel):
    organization: OrganizationCreate
    user: UserCreate
