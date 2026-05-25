```python

@router.post("/save", response_model=TimesheetCreateResponse, status_code=status.HTTP_201_CREATED)
# save endpoint is separate from submit endpoint to allow users to save drafts without submitting for approval.
def create_timesheet_save(
    payload: TimesheetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status = db.query(Timesheet.status).filter(Timesheet.user_project_mapping_id == payload.user_project_mapping_id).order_by(Timesheet.work_date.desc()).first()
    
    if status and status[0]=="Submitted":
        raise HTTPException(status_code=400, detail="cannot updte timesheet for a project with already submitted timesheet, please contact manager")
    ts = create_timesheet_service(db, current_user.id, payload)
    return TimesheetCreateResponse(message="Timesheet created successfully", data=ts)

```
