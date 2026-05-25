from services.auth_service import get_current_user
from sqlalchemy.orm import Session
from datetime import datetime, date, timedelta
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from database.models import Timesheet, User, UserProjectMapping
from schemas.timesheet import (
    TimesheetCreate,
    TimesheetWeeklyCreate,
    TimesheetUpdate,
)

# CREATE TIMESHEET
def create_timesheet_service(db: Session, user_id: int, data: TimesheetCreate):
    """Create a new timesheet row for the current user via their project mapping."""
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.user_project_mapping_id is None:
        raise HTTPException(
            status_code=400,
            detail="user_project_mapping_id is required to create a timesheet",
        )

    mapping = db.query(UserProjectMapping).get(data.user_project_mapping_id)
    if not mapping:
        raise HTTPException(
            status_code=400,
            detail="Invalid user_project_mapping_id (mapping not found)",
        )

    if int(mapping.user_id) != int(user.id):
        raise HTTPException(
            status_code=403,
            detail="user_project_mapping_id does not belong to current user",
        )

    ts = Timesheet(
        user_project_mapping_id=data.user_project_mapping_id,
        work_date=data.work_date,
        hours_worked=data.hours_worked,
        description=data.description,
        status="Draft",
    )
    db.add(ts)
    try:
        db.commit()
        db.refresh(ts)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not create timesheet (invalid mapping or duplicate entry)",
        )
    return ts

#weekly save
def weekly_save_service(db: Session, user_id: int, payload: TimesheetWeeklyCreate):
    """Upsert many timesheet rows for the current user (same mapping + calendar day = update)."""
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not payload.timesheets:
        raise HTTPException(status_code=400, detail="timesheets list cannot be empty")

    validated = []
    for entry in payload.timesheets:
        if entry.user_project_mapping_id is None:
            raise HTTPException(
                status_code=400,
                detail="user_project_mapping_id is required for each entry",
            )
        mapping = db.query(UserProjectMapping).get(entry.user_project_mapping_id)
        if not mapping:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid user_project_mapping_id: {entry.user_project_mapping_id}",
            )
        if int(mapping.user_id) != int(user.id):
            raise HTTPException(
                status_code=403,
                detail="One or more mappings do not belong to the current user",
            )
        work_day = (
            entry.work_date.date()
            if hasattr(entry.work_date, "date")
            else entry.work_date
        )
        validated.append((entry, work_day))

    saved: list = []
    try:
        for entry, work_day in validated:
            ts = (
                db.query(Timesheet)
                .filter(
                    Timesheet.user_project_mapping_id == entry.user_project_mapping_id,
                    func.date(Timesheet.work_date) == work_day,
                )
                .first()
            )

            if ts:
                status_lower = (ts.status or "").lower()
                if status_lower in ("submitted", "approved"):
                    raise HTTPException(
                        status_code=400,
                        detail="Cannot update a submitted or approved timesheet entry",
                    )
                ts.hours_worked = entry.hours_worked
                ts.description = entry.description
                saved.append(ts)
            else:
                new_ts = Timesheet(
                    user_project_mapping_id=entry.user_project_mapping_id,
                    work_date=entry.work_date,
                    hours_worked=entry.hours_worked,
                    description=entry.description,
                    status="Draft",
                )
                db.add(new_ts)
                saved.append(new_ts)

        db.commit()
    except HTTPException:
        db.rollback()
        raise
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not save weekly timesheets (database constraint)",
        )

    for ob in saved:
        db.refresh(ob)
    return saved

#submit weekly timesheet
def submit_weekly_timesheet_service(
    db: Session,
    user_id: int,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    """Submit weekly timesheet entries by updating only their status."""
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if start_date is None or end_date is None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        start_date = start_date or week_start
        end_date = end_date or today

    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="Invalid date range: start_date must be before or equal to end_date",
        )

    timesheets = (
        db.query(Timesheet)
        .join(UserProjectMapping, Timesheet.user_project_mapping_id == UserProjectMapping.id)
        .filter(
            UserProjectMapping.user_id == user_id,
            func.date(Timesheet.work_date) >= start_date,
            func.date(Timesheet.work_date) <= end_date,
        )
        .all()
    )

    if not timesheets:
        raise HTTPException(
            status_code=404,
            detail="No weekly timesheet entries found for the selected date range",
        )

    updated = []
    for ts in timesheets:
        if (ts.status or "").lower() in ("submitted", "approved"):
            continue
        ts.status = "Submitted"
        ts.submitted_at = datetime.utcnow()
        updated.append(ts)

    if not updated:
        raise HTTPException(
            status_code=400,
            detail="No draft weekly timesheet entries available to submit",
        )

    db.commit()
    for ts in updated:
        db.refresh(ts)
    return updated

#submit timesheet by user
def submit_timesheet_service(
    db: Session,
    ts_id: int,
    user_id: int,
) -> Timesheet | None:
    """
    Submit a single timesheet by id for the given user.

    Ownership is checked via UserProjectMapping.user_id.
    """
    row = (
        db.query(Timesheet, UserProjectMapping)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .filter(
            Timesheet.timesheet_id == ts_id,
            UserProjectMapping.user_id == user_id,
        )
        .first()
    )

    if not row:
        return None

    ts, _ = row
    status_lower = (ts.status or "").lower()
    if status_lower in ("submitted", "approved"):
        return ts

    ts.status = "Submitted"
    ts.submitted_at = datetime.now()
    db.commit()
    db.refresh(ts)
    return ts


#update timesheet by user
def update_timesheet_service(
    db: Session, ts_id: int, user_id: int, data: TimesheetUpdate
):
    """
    Update a timesheet owned by the user (via user_project_mapping).
    Timesheet has no user_id/project_id columns; authorization uses the mapping row.
    """
    row = (
        db.query(Timesheet, UserProjectMapping)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .filter(
            Timesheet.timesheet_id == ts_id,
            UserProjectMapping.user_id == user_id,
        )
        .first()
    )

    if not row:
        return None

    ts, mapping = row
    status_lower = (ts.status or "").lower()
    if status_lower in ("submitted", "approved"):
        raise HTTPException(
            status_code=400,
            detail="Cannot update a submitted or approved timesheet",
        )

    patch = data.model_dump(exclude_unset=True)

    if patch.get("project_id") is not None:
        if int(mapping.project_id) != int(patch["project_id"]):
            raise HTTPException(
                status_code=400,
                detail="project_id does not match this timesheet's user–project mapping",
            )

    for field in ("work_date", "hours_worked", "description", "status"):
        if field in patch and patch[field] is not None:
            setattr(ts, field, patch[field])

    for field in ("approved_by", "approved_at"):
        if field in patch and patch[field] is not None:
            setattr(ts, field, patch[field])

    try:
        db.commit()
        db.refresh(ts)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not update timesheet (database constraint)",
        )
    return ts






#approve timesheet by manager
def approve_timesheet_services(db: Session, ts_id: int, manager_id: int) -> Timesheet | None:
    """
    Approve a submitted timesheet where the employee reports to this manager.

    The Timesheet model has no user_id/manager_id columns, so we enforce
    the relationship via UserProjectMapping → User.manager_id.
    """
    row = (
        db.query(Timesheet, UserProjectMapping, User)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .join(User, UserProjectMapping.user_id == User.id)
        .filter(
            Timesheet.timesheet_id == ts_id,
            Timesheet.status == "Submitted",
            User.manager_id == manager_id,
        )
        .first()
    )

    if not row:
        return None

    ts, _, _ = row
    ts.status = "Approved"
    ts.approved_at = datetime.now()
    db.commit()
    db.refresh(ts)
    return ts

#reject timesheet by manager
def reject_timesheet_services(db: Session, ts_id: int, manager_id: int) -> Timesheet | None:
    """
    Reject a submitted timesheet where the employee reports to this manager.
    """
    row = (
        db.query(Timesheet, UserProjectMapping, User)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .join(User, UserProjectMapping.user_id == User.id)
        .filter(
            Timesheet.timesheet_id == ts_id,
            Timesheet.status == "Submitted",
            User.manager_id == manager_id,
        )
        .first()
    )

    if not row:
        return None

    ts, _, _ = row
    ts.status = "Rejected"
    db.commit()
    db.refresh(ts)
    return ts


#update timesheet by manager
def update_timesheet_service(db: Session, ts_id: int, user_id: int, data: TimesheetUpdate):
    """
    Update a timesheet owned by the user (via user_project_mapping).
    Timesheet has no user_id/project_id columns; authorization uses the mapping row.
    """
    row = (
        db.query(Timesheet, UserProjectMapping)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .filter(
            Timesheet.timesheet_id == ts_id,
            UserProjectMapping.user_id == user_id,
        )
        .first()
    )

    if not row:
        return None

    ts, mapping = row
    status_lower = (ts.status or "").lower()
    if status_lower in ("submitted", "approved"):
        raise HTTPException(
            status_code=400,
            detail="Cannot update a submitted or approved timesheet",
        )

    patch = data.model_dump(exclude_unset=True)

    if patch.get("project_id") is not None:
        if int(mapping.project_id) != int(patch["project_id"]):
            raise HTTPException(
                status_code=400,
                detail="project_id does not match this timesheet's user–project mapping",
            )

    for field in ("work_date", "hours_worked", "description", "status"):
        if field in patch and patch[field] is not None:
            setattr(ts, field, patch[field])

    for field in ("approved_by", "approved_at"):
        if field in patch and patch[field] is not None:
            setattr(ts, field, patch[field])

    try:
        db.commit()
        db.refresh(ts)
    except IntegrityError:
        db.rollback()









 
# get weekly timesheets
def get_weekly_timesheets_services(
    db: Session, user_id: int, week: int = 0
) -> list[Timesheet]:
    """
    Get all timesheets for a given week offset for the current user.

    week = 0 → current week, 1 → previous week, etc.
    """
    today = date.today()
    # Monday of current week, then shift by `week` weeks back
    current_week_start = today - timedelta(days=today.weekday())
    week_start = current_week_start - timedelta(weeks=week)
    week_end = week_start + timedelta(days=6)

    timesheets = (
        db.query(Timesheet)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .filter(
            UserProjectMapping.user_id == user_id,
            Timesheet.work_date >= week_start,
            Timesheet.work_date <= week_end,
        )
        .order_by(Timesheet.work_date)
        .all()
    )
    return timesheets

# get pending reviews
def get_pending_reviews_services(db: Session, manager_id: int) -> list[Timesheet]:
    """
    Get all SUBMITTED timesheets for employees who report to this manager.

    Uses User.manager_id to find subordinates, then their mappings and timesheets.
    """
    # Find all direct reports for this manager
    subordinate_ids = (
        db.query(User.id).filter(User.manager_id == manager_id).all()
    )
    subordinate_ids = [row.id for row in subordinate_ids]

    if not subordinate_ids:
        return []

    # Timesheets whose mapping belongs to any subordinate and are in Submitted status
    rows = (
        db.query(Timesheet)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .filter(
            UserProjectMapping.user_id.in_(subordinate_ids),
            Timesheet.status == "Submitted",
        )
        .order_by(Timesheet.work_date)
        .all()
    )
    return rows
    
def update_timesheet_services(db: Session, ts_id: int, user_id: int, data: TimesheetUpdate):
    """
    Update a timesheet owned by the user (via user_project_mapping).
    Timesheet has no user_id/project_id columns; authorization uses the mapping row.
    """
    row = (
        db.query(Timesheet, UserProjectMapping)
        .join(
            UserProjectMapping,
            Timesheet.user_project_mapping_id == UserProjectMapping.id,
        )
        .filter(
            Timesheet.timesheet_id == ts_id,
            UserProjectMapping.user_id == user_id,
        )
        .first()
    )

    if not row:
        return None

    ts, mapping = row
    status_lower = (ts.status or "").lower()
    if status_lower in ("submitted", "approved"):
        raise HTTPException(
            status_code=400,
            detail="Cannot update a submitted or approved timesheet",
        )

    patch = data.model_dump(exclude_unset=True)

    if patch.get("project_id") is not None:
        if int(mapping.project_id) != int(patch["project_id"]):
            raise HTTPException(
                        status_code=400,
                detail="project_id does not match this timesheet's user–project mapping",
            )

    for field in ("work_date", "hours_worked", "description", "status"):
        if field in patch and patch[field] is not None:
            setattr(ts, field, patch[field])

    for field in ("approved_by", "approved_at"):
        if field in patch and patch[field] is not None:
            setattr(ts, field, patch[field])

    try:   
        db.commit()
        db.refresh(ts)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="Could not update timesheet (database constraint)",
        )
    return ts
