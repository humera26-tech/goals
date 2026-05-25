from datetime import date
from typing import Optional
from pydantic import BaseModel


class AchievementBase(BaseModel):
    title: str
    description: Optional[str] = None
    awarded_date: Optional[date] = None
    awarded_by_id: Optional[int] = None  # FK to users.id (manager/coach/etc.)


class AchievementCreate(AchievementBase):
    pass


class AchievementOut(AchievementBase):
    id: int
    user_id: int
    model_config = {"from_attributes": True}
