from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TimesheetCreate(BaseModel):
   
    user_project_mapping_id:Optional[int] = None
    work_date: datetime
    hours_worked: float
    description: Optional[str] = None
    
#employee save
class TimesheetSave(BaseModel):
    pass    


#employee update
class TimesheetUpdate(BaseModel):
    task_id: Optional[int]
    project_id: Optional[int]
    work_date: Optional[datetime]
    hours_worked: Optional[float]
    description: Optional[str]
    status: Optional[str]
    approved_by: Optional[int]
    approved_at: Optional[datetime]

#employee submit
class TimesheetSubmit(BaseModel):
    submit:bool #true submit to manager
    

class TimesheetWeeklyCreate(BaseModel):
    timesheets: List[TimesheetCreate]


class TimesheetResponse(BaseModel):
    timesheet_id: int
   
    user_project_mapping_id: int
    work_date: datetime
    hours_worked: float
    description: Optional[str]
    status: str
    submitted_at: datetime
    approved_by: Optional[int]
    approved_at: Optional[datetime]

    class Config:
        from_attributes = True


class TimesheetWeeklySaveResponse(BaseModel):
    message: str
    data: List[TimesheetResponse]


class TimesheetApproval(BaseModel):
    action: str #approve or reject    

    class Config:
        from_attributes = True

class TimesheetReviewResponse(BaseModel):
    message: str
    data: List[TimesheetResponse]
    class Config:
        from_attributes = True

        