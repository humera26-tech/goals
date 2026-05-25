from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database import models
from schemas.education import EducationCreate, EducationUpdate, EducationOut
from services.user_service import _check_can_access_details

# add education details of user
def add_education_for_user(
    db: Session,
    current_user: models.User,
    user_id: int,
    payload: EducationCreate,
) -> EducationOut:
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    _check_can_access_details(current_user, target_user)

    edu = models.Education(
        user_id=user_id,
        level=payload.level,
        institution=payload.institution,
        degree=payload.degree,
        field_of_study=payload.field_of_study,
        start_date=payload.start_date,
        end_date=payload.end_date,
        grade=payload.grade,
    )

    db.add(edu)
    db.commit()
    db.refresh(edu)

    return EducationOut.from_orm(edu)

# list of educations of user
def list_education_for_user(
    db: Session,
    current_user: models.User,
    user_id: int,
) -> list[EducationOut]:
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    _check_can_access_details(current_user, target_user)
    educations = (
        db.query(models.Education)
        .filter(models.Education.user_id == user_id)
        .order_by(models.Education.start_date)
        .all()
    )

    return educations


# update  education of user
def update_education_for_user(
    db: Session,
    current_user: models.User,
    user_id: int,
    education_id: int,
    payload: EducationUpdate,
):
    #user Validation and Permission Check
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    _check_can_access_details(current_user, target_user)

    # payload.model_dump(exclude_unset=True) ensures only fields passed by the user are included.
    data = payload.model_dump(exclude_unset=True)

    #Direct SQL Update using .update()
    rows_updated = (
        db.query(models.Education)
        .filter(
            models.Education.id == education_id,
            models.Education.user_id == user_id,
        )
        # Execute the UPDATE statement directly against the database
        .update(data, synchronize_session=False)
    )

    if rows_updated == 0:
        db.rollback() # Rollback if no rows were updated before raising an error
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Education record not found or does not belong to the user"
        )

    # Commit the transaction that contains the SQL UPDATE
    db.commit()

    # Fetch the updated record
    # We must explicitly fetch the record because .update() doesn't update the Python object.
    edu = (
        db.query(models.Education)
        .filter(models.Education.id == education_id)
        .first()
    )

    return EducationOut.from_orm(edu)
# delete education of user
def delete_education_for_user(
    db: Session,
    current_user: models.User,
    user_id: int,
    education_id: int,
) -> None:
    target_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    _check_can_access_details(current_user, target_user)

    edu = (
        db.query(models.Education)
        .filter(
            models.Education.id == education_id,
            models.Education.user_id == user_id,
        )
        .first()
    )
    if not edu:
        raise HTTPException(status_code=404, detail="Education record not found")

    db.delete(edu)
    db.commit()
