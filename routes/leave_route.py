from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from schemas.leave import LeaveCreate, LeaveResponse
from services.leave_services import create_leave, get_all_leaves
from services.auth_service import get_current_user

router = APIRouter(
    tags=["Leaves"]


)

@router.post(
    "/",
    status_code=status.HTTP_200_OK
)
def create_leave_api(
    payload: LeaveCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    create_leave(db, payload, current_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Leave created successful"})


@router.get(
    "/",
    response_model=List[LeaveResponse]
)
def get_leaves_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_all_leaves(db)


    