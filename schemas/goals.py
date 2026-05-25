
from enum import Enum
from datetime import date, datetime
from typing import Optional,List,Literal
from pydantic import BaseModel,ConfigDict
from datetime import datetime

class Goal_Create(BaseModel):
    title: str
    description: Optional[str] = None
    goal_type: str = "Indiviual"  # e.g., "personal", "professional", etc.
    start_date: date = date.today()
    end_date: Optional[date] = None

    status: Optional[str] = None  # e.g., "not started", "in progress", "completed"
    progress: Optional[int] = 0  # 0 to 100
    created_at: datetime  # user_id of the creator
  

class Goal_Update(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    goal_type: Optional[str] = None
    end_date: Optional[date] = None
    status: Optional[str] = None
    progress: Optional[int] = None
  
 

class Goal_Response(BaseModel):

    id: int
    title: str
    description: Optional[str] = None
    goal_type: List[Literal["Individual", "Team"]]
    start_date: date =datetime.now()
    end_date: Optional[date] = None
    status: Optional[str] = None
    created_at: datetime
    user_id: int


    