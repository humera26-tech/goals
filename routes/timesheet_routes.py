import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.database import get_db
from database.models import Role, Timesheet, User,UserProjectMapping
from schemas.message import TimesheetCreateResponse, TimesheetUpdateResponse
from schemas.timesheet import (
    TimesheetCreate,
    TimesheetUpdate,
    TimesheetWeeklyCreate,
    TimesheetWeeklySaveResponse,
)
from services.auth_service import get_current_user
from services.timesheet_service import create_timesheet_service,update_timesheet_service, weekly_save_service, approve_timesheet_services ,get_weekly_timesheets_services
router = APIRouter(prefix="/timesheets", tags=["Timesheets"])

@router.get("/me", response_model=TimesheetWeeklySaveResponse, status_code=status.HTTP_200_OK)
def get_user_timesheets(
    week: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mapping = db.query(UserProjectMapping).filter(
        UserProjectMapping.user_id == current_user.id
    ).first()
    
    if not mapping:
        raise HTTPException(status_code=404, detail="User project mapping not found")
    
    return get_weekly_timesheets_services(db, mapping.id, week)


@router.post(
    "/weekly-save",
    response_model=TimesheetWeeklySaveResponse,
    status_code=status.HTTP_200_OK,
)
def weekly_save(
    payload: TimesheetWeeklyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    rows = weekly_save_service(db, current_user.id, payload)
    return TimesheetWeeklySaveResponse(
        message="Weekly timesheets saved successfully",
        data=rows,
    )


@router.put("/{id}/approve", response_model=TimesheetUpdateResponse)
def approve_timesheet_api(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ts = db.query(Timesheet).filter(Timesheet.id == id).first()
    if not ts:
        raise HTTPException(status_code=404, detail="Timesheet not found")
    
    role = db.query(Role.role_name).filter(Role.id == current_user.role_id).first()
    if not role or role[0] != "Manager":
        raise HTTPException(status_code=403, detail="Only managers can approve timesheets")
    
    if ts.status != "Submitted":
        raise HTTPException(status_code=400, detail="Only submitted timesheets can be approved")
    
    ts.status = "Approved"
    db.commit()
    db.refresh(ts)
    return TimesheetUpdateResponse(message="Timesheet approved successfully", data=ts)
        
        



#filter data range
# @router.post("/filter")
# def filter_timesheet(filter_data:TimesheetFilter, db: Session = Depends(get_db)):
#     return
#     TimesheetService.get_timeshets_by_filter
#     (
#          db, 
#         filter_data.user_id,
#         filter_data.start_date,
#         filter_data.end_date
#     )  
#submit week
# @router.post("/submit")  
# def submit_timesheet(filte_data:TimesheetFilter, db: Session = Depends(get_db)):
#     return
#     TimesheetService.submit_week_timesheet(
#         db,
#         filter_data.user_id, 
#         filte_data.start_date, 
#         filte_data.end_date
#     )
   



@router.post("/{id}/submit")
def submit_timesheet_api(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    submit=db.query(Timesheet).filter(Timesheet.id == id, Timesheet.user_id == current_user.id).first() 
    if not submit:
        raise HTTPException(status_code=404, detail="Timesheet not found or not authorized")
    submit.status="Submitted"
    db.commit()
    db.refresh(submit)
    return {"message": "Timesheet submitted successfully"}  
    


# @router.get("/manager/submitted")
# def manager_view_api(
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Manager timesheet view API not implemented yet",
#     )


# @router.post("/{ts_id}/{action}")
# def approve_reject_api(
#     id: int,
#     action: str,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user),
# ):
#     raise HTTPException(
#         status_code=status.HTTP_501_NOT_IMPLEMENTED,
#         detail="Timesheet approve/reject API not implemented yet",
#     )
#     return approve_timesheet_services(db, id, action, current_user.id)
     
