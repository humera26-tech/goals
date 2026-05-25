from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from decimal import Decimal


# Base Schema
class UserProjectMappingBase(BaseModel):
    user_id: int
    project_id: int
    role: str = Field(..., max_length=50)
    billable: bool = False
    allocation_percent: Decimal = Field(..., ge=0, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# Create Schema
class UserProjectMappingCreate(UserProjectMappingBase):
    pass


# Update Schema
class UserProjectMappingUpdate(BaseModel):
    role: Optional[str] = Field(None, max_length=50)
    billable: Optional[bool] = None
    allocation_percent: Optional[Decimal] = Field(None, ge=0, le=100)
    start_date: Optional[date] = None
    end_date: Optional[date] = None


# Response Schema
class UserProjectMappingResponse(UserProjectMappingBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

