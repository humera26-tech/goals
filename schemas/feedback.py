from enum import Enum
from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel

class Feedback_Create(BaseModel):
    
    reviewer_name: str
    review_period: str
    overall_rating: float
    strengths: Optional[str] = None
    improvement: Optional[str] = None
    created_at: datetime = datetime.now()
