from enum import Enum
from datetime import date
from typing import Optional
from pydantic import BaseModel


class EducationLevel(str, Enum):
    undergraduate = "undergraduate"
    postgraduate = "postgraduate"
    other = "other"   # diplomas, certifications, etc.


class EducationBase(BaseModel):
    level: EducationLevel
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = None


class EducationCreate(EducationBase):
    pass

class EducationUpdate(BaseModel):
    # level: Optional[EducationLevel] = None
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    grade: Optional[str] = None


class EducationOut(EducationBase):
    id: int
    user_id: int
    model_config = {"from_attributes": True}
