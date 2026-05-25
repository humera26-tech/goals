from sqlalchemy.orm import Session
from schemas.leaverequests import LeaveCreate
from database.models import LeaveRequests
from fastapi import HTTPException


def create_leave(db: Session, leave: LeaveCreate):

    if leave.is_half_day:
        if not leave.half_day_type or leave.half_day_type not in ["first_half", "second_half"]:
            raise HTTPException(
                status_code=400,
                detail="half_day_type must be 'first_half' or 'second_half' when is_half_day is True"
            )

    new_leave = LeaveRequests(
        user_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        total_days=leave.total_days,
        reason=leave.reason,
        half_day=leave.is_half_day,
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)
    return new_leave


def get_all_leaves(db: Session):
    return db.query(LeaveRequests).all()


def get_leave_by_id(db: Session, leave_id: int):
    return db.query(LeaveRequests).filter(LeaveRequests.id == leave_id).first()


def update_leave(db:Session,leave_id:int,data:LeaveUpdate):
    leave=get_leave_by_id(db,leave_id)
    if not leave:
        return None
    #raise HTTPException(status_code=404,detail="Leave  not found")
    if data.start_date is not None:
        leave.start_date=data.start_date   
    if data.end_date is not None:
        leave.end_date=data.end_date
    if data.leave_type is not None:
        leave.leave_type=data.leave_type
    if data.status is not None:
        leave.status=data.status
    if data.approved_by is not None:
        leave.approved_by=data.approved_by    
       
        
    db.commit()
    db.refresh(leave)
    return leave
