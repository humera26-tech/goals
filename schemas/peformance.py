from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PerformanceReviewBase(BaseModel):
    user_id: int
    reviewer_id: int
    review_period: str
    overall_rating: float
    strengths: Optional[str]
    improvements: Optional[str]


class PerformanceReviewCreate(PerformanceReviewBase):
    pass


class PerformanceReviewUpdate(BaseModel):
    review_period: Optional[str]
    overall_rating: Optional[float]
    strengths: Optional[str]
    improvements: Optional[str]
    


class PerformanceReviewResponse(PerformanceReviewBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True