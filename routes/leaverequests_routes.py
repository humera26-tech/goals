from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.leaverequests import LeaveCreate, LeaveResponse
from services.leaverequests_service import (
    create_leave,
    get_all_leaves,
    get_leave_by_id 
)

#router = APIRouter(prefix="/leaves", tags=["Leaves"])
router = APIRouter(tags=["Leave_requests"])



@router.post("/", response_model=LeaveResponse)
def create_leave_request(
    leave: LeaveCreate,
    db: Session = Depends(get_db)
):
    return create_leave(db, leave)


@router.get("/", response_model=list[LeaveResponse])
def read_all_leaves(db: Session = Depends(get_db)):
    return get_all_leaves(db)


@router.get("/{leave_id}", response_model=LeaveResponse)
def read_leave_by_id(
    leave_id: int,
    db: Session = Depends(get_db)
):
    leave = get_leave_by_id(db, leave_id)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")
    return leave

@router.put("/{leave_id}", response_model=LeaveResponse)
def update(leave_id:int, data:LeaveUpdate, db:Session=Depends(get_db)):
    leave=update_leave(db, leave_id, data)
    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    return leave



    