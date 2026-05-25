from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from database import models
from utils import hash_password


def register_org_with_user_service(db: Session, payload=None):
    org_data = payload.organization
    user_data = payload.user

    # Check for existing org (same prefix or email)
    existing_org = (
        db.query(models.Organization)
        .filter(
            (models.Organization.org_prefix == org_data.org_prefix)
            | (models.Organization.email == org_data.email)
        )
        .first()
    )
    if existing_org:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization with same prefix or email already exists",
        )

    # Check for existing user (same work_email)
    existing_user = (
        db.query(models.User)
        .filter_by(work_email=user_data.work_email)
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this work_email already exists",
        )

    try:
        org = models.Organization(**org_data.dict())
        db.add(org)
        db.flush()
        # Create Role for this org
        role = models.Role(
            role_name=user_data.role_name,
            org_id=org.id,
        )
        db.add(role)
        db.flush()

        # Create User linked to org + role
        hashed_password = hash_password(user_data.password)
        user = models.User(
            work_email=user_data.work_email,
            username=user_data.username,
            title=user_data.title,
            department=user_data.department,
            hashed_password=hashed_password,
            org_id=org.id,
            role_id=role.id,
        )
        db.add(user)

        db.commit()

        db.refresh(org)
        db.refresh(role)
        db.refresh(user)
    except Exception as e :
        db.rollback()
        raise e


