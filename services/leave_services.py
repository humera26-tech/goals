
from sqlalchemy.orm import Session
from database import models
from schemas.leave import LeaveCreate

def create_leave(db: Session, payload: LeaveCreate, current_user: models.User):
    # Create Leave record
    leave = models.Leave(
        user_id=current_user.id,
        leave_name=payload.leave_name,
        max_days_per_year=payload.max_days_per_year,
        is_paid=payload.is_paid,
        allow_half_day=payload.allow_half_day,
        is_active=payload.is_active,
    )
    db.add(leave)
    db.flush()  # Flush to get the leave ID if needed, but don't commit yet
    
    # Create LeaveRequest record
    leave_request = models.LeaveRequests(
        user_id=current_user.id,
        leave_type=payload.leave_name,
        start_date=payload.start_date,
        end_date=payload.end_date,
        total_days=payload.total_days,
        reason=payload.reason,
        half_day=payload.is_half_day,
        status=models.LeaveStatus.PENDING,
    )
    db.add(leave_request)
    db.commit()
    db.refresh(leave)
    db.refresh(leave_request)
    return leave


def get_all_leaves(db: Session):
    return db.query(models.Leave).all()