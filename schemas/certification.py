from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from datetime import datetime, date, timedelta



class CertificationBase(BaseModel):
    name: str
    status: str 
    provider: Optional[str] = None
    
    planned_date: Optional[date] = None
    completed_date: Optional[date] = None
    expiry_date: Optional[date] = None

    @model_validator(mode='after')
    def validate_certification_dates(self):
        """Validate that required dates are provided based on status."""
        if self.status == "upcoming" and self.planned_date is None:
            raise ValueError("planned_date is required when status is 'upcoming'")
        
        if self.status == "completed":
            if self.completed_date is None:
                raise ValueError("completed_date is required when status is 'completed'")
            if self.expiry_date is None:
                raise ValueError("expiry_date is required when status is 'completed'")
        
        if self.status == "expired" and self.expiry_date is None:
            raise ValueError("expiry_date is required when status is 'expired'")
        
        return self


class CertificationCreate(CertificationBase):
    pass


class CertificationUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[str] = None
    provider: Optional[str] = None
    planned_date: Optional[date] = None
    completed_date: Optional[date] = None
    expiry_date: Optional[date] = None


class CertificationOut(BaseModel):
    pass

class CertificationResponse(BaseModel):
    id: int
    user_id: int
    name: str
    provider: str
    status: str
    planned_date: Optional[date] = None
    completed_date: Optional[date] = None
    expiry_date: Optional[date] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
