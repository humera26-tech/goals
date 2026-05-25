from pydantic import BaseModel, Field
from typing import Optional,Annotated
from datetime import datetime, date

class LeaveBase(BaseModel):
    leave_name: Annotated[str, Field(..., description="Name of the leave type")]
    max_days_per_year: Annotated[int, Field(..., description="Maximum number of days allowed per year")] 
    is_paid: Optional[bool] = True
    allow_half_day: Optional[bool] = False
    is_active: Optional[bool] = True


class LeaveCreate(LeaveBase):
    leave_name: Annotated[str, Field(..., description="Name of the leave type")]
    max_days_per_year: Annotated[int, Field(..., description="Maximum number of days allowed per year")]
    # Fields for LeaveRequest
    start_date: Annotated[date, Field(..., description="Start date of the leave request")]
    end_date: Annotated[date, Field(..., description="End date of the leave request")]
    total_days: Annotated[int, Field(..., description="Total number of days for the leave request")]
    reason: Optional[str] = None
    is_half_day: Optional[bool] = False

class LeaveResponse(LeaveBase):
    id: int
    created_at: datetime
    updated_at: datetime

class Config:
        from_attributes = True