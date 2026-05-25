from pydantic import BaseModel,Field,model_validator
from datetime import date, datetime
from typing import Optional,Any


class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    total_days: int
    reason: Optional[str] = None
    is_half_day: bool = False
    half_day_type: Optional[str] = None  # first_half | second_half


class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    total_days: int
    reason: Optional[str]
    status: str
    is_half_day: bool
    half_day_type: Optional[str]= None
    applied_on: datetime
    created_at: datetime

    @model_validator(mode='before')
    @classmethod
    def transform_fields(cls, data: Any) -> Any:
        if isinstance(data, dict):
            #map user_id to employee_id
            if 'user_id' in data:
                data['employee_id'] = data.pop('user_id')
            #map half_day to is_half_day
            if 'half_day' in data:
                data['is_half_day'] = data.pop('half_day')
            #convert status enum to string if needed   
            if 'status' in data and hasattr(data['status'], 'value'):
                data['status'] = data['status'].value
        elif hasattr(data, '__dict__'): 
            #handle ORM objects 
            obj_dict=data.__dict__.copy()
            if hasattr(data, 'user_id'):
                obj_dict['employee_id'] = data.user_id
            if hasattr(data, 'half_day'): 
                obj_dict['is_half_day'] = data.half_day
            if hasattr(data, 'status') and hasattr(data.status, 'value'):
                obj_dict['status'] = data.status.value

            return 
        return data         

    class Config:
        orm_mode = True