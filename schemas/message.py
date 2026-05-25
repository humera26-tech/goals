from pydantic import BaseModel, EmailStr
from typing import Optional
from schemas.certification import CertificationResponse, CertificationUpdate
from schemas.timesheet import TimesheetResponse
from schemas.project import ProjectResponse, ProjectUpdate, ProjectCreate
from datetime import datetime
from typing import List
from schemas.userprojectmapping import UserProjectMappingResponse, UserProjectMappingUpdate, UserProjectMappingCreate

class MessageResponse(BaseModel):
    message: str


class CertificationCreateResponse(BaseModel):
    message: str
    data: CertificationResponse


class CertificationUpdateResponse(BaseModel):
    message: str
    data: CertificationResponse


class TimesheetCreateResponse(BaseModel):
    message: str
    data: TimesheetResponse


class TimesheetUpdateResponse(BaseModel):
    message: str
    data: TimesheetResponse




class ProjectCreateResponse(BaseModel):
    message: str
    data: ProjectResponse


class ProjectUpdateResponse(BaseModel):
    message: str
    data: ProjectResponse    


class UserProjectMappingCreateResponse(BaseModel):
    message: str
    data: UserProjectMappingResponse

class UserProjectMappingUpdateResponse(BaseModel):
    message: str
    data: UserProjectMappingResponse    