from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum
class ProjectStatus(str, Enum):
    active = "active"
    inactive = "inactive"
    completed = "completed"

class ProjectCreate(BaseModel):
    name: str
    user_id: int
    description: Optional[str] = None
    project_type: Optional[str]
    client_id: Optional[int]
    billable_flag: Optional[bool] = False
    internal_project_flag: Optional[bool] = False
    created_at: datetime
    org_id: Optional[int] = None
    status: ProjectStatus=ProjectStatus.active
    

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None    
    project_type: Optional[str]
    billable_flag:Optional[bool]
    internal_project_flag:Optional[bool]

class ProjectResponse(BaseModel):
    project_id: int
    project_name: str
    description: Optional[str] = None
    created_at: datetime
    status: str

    class Config:
        from_attributes = True


class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]

    class Config:
        from_attributes = True

