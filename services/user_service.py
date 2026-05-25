from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from database import models
from schemas.user import UserBasicOut, ChangePasswordRequest, UserCreateInOrg
from services.achievement_service import create_achievement_for_user
from utils import verify_password, hash_password
from schemas.user import (
    UserDetailsCreate,
    UserDetailsUpdate,
    UserDetailsOut,
)
from schemas.achievement import AchievementCreate, AchievementOut
def get_basic_details_user_service(current_user: models.User) -> UserBasicOut:
    return UserBasicOut.from_orm(current_user)

# chanage password service
def change_password_service(
    db: Session, current_user: models.User, payload: ChangePasswordRequest,
):
    # Make sure this matches your User model field
    current_hashed = current_user.hashed_password

    # Check old password
    if not verify_password(payload.old_password, current_hashed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect",
        )

    # Prevent same password reuse
    if verify_password(payload.new_password, current_hashed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="New password must be different from old password",
        )

    # Hash & update
    new_hashed = hash_password(payload.new_password)
    current_user.hashed_password = new_hashed

    db.add(current_user)
    db.commit()
    
# add new user in existing organization
def create_user_in_org_service(db: Session, current_user: models.User, payload: UserCreateInOrg,) -> UserBasicOut:

    # Ensure current_user is an Owner
    if not current_user.role or current_user.role.role_name.lower() != "owner":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only organization owner can add users",
        )

    org_id = current_user.org_id

    # Ensure email and username not already used
    existing_by_email = (
        db.query(models.User)
        .filter(models.User.work_email == payload.work_email.lower())
        .first()
    )
    if existing_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists",
        )

    existing_by_username = (
        db.query(models.User)
        .filter(models.User.username == payload.username)
        .first()
    )
    if existing_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )

    # Get or create role for this org (based on role_name from payload)
    target_role_name = payload.role_name or "Member"

    role = (
        db.query(models.Role)
        .filter(
            models.Role.org_id == org_id,
            models.Role.role_name == target_role_name,
        )
        .first()
    )

    if not role:
        role = models.Role(
            role_name=target_role_name,
            org_id=org_id,
        )
        db.add(role)
        db.flush()
        
    # Hash password and create user
    hashed_pw = hash_password(payload.password)

    new_user = models.User(
        work_email=payload.work_email.lower(),
        username=payload.username,
        title=payload.title,
        department=payload.department,
        hashed_password=hashed_pw,
        org_id=org_id,
        role_id=role.id,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserBasicOut.from_orm(new_user)


def _get_user_or_404(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


def _check_can_access_details(current_user: models.User, target_user: models.User) -> None:
    is_self = current_user.id == target_user.id
    is_owner_same_org = (
        current_user.org_id == target_user.org_id
        and current_user.role
        and current_user.role.role_name.lower() == "owner"
    )

    if not (is_self or is_owner_same_org):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not allowed to manage this user's details",
        )


def create_user_details(
    db: Session,
    current_user: models.User,
    user_id: int,
    payload: UserDetailsCreate,
) -> UserDetailsOut:
    target_user = _get_user_or_404(db, user_id)
    _check_can_access_details(current_user, target_user)

    existing = (
        db.query(models.UserDetails)
        .filter(models.UserDetails.user_id == user_id)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Details already exist. Use update instead.",
        )

    details = models.UserDetails(
        user_id=user_id,
        personal_email=payload.personal_email,
        dob=payload.dob,
        pwd_flag=payload.pwd_flag,
        maritalstatus_flag=payload.maritalstatus_flag,
        gender=payload.gender,
        nationality=payload.nationality,
        address=payload.address,
        blood_group=payload.blood_group,
    )

    db.add(details)
    db.commit()
    db.refresh(details)

    return UserDetailsOut.from_orm(details)


def get_user_details(
    db: Session,
    current_user: models.User,
    user_id: int,
) -> UserDetailsOut:
    target_user = _get_user_or_404(db, user_id)
    _check_can_access_details(current_user, target_user)

    details = (
        db.query(models.UserDetails)
        .filter(models.UserDetails.user_id == user_id)
        .first()
    )
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User details not found",
        )

    return UserDetailsOut.from_orm(details)

def update_user_details(db: Session,current_user: models.User,
    user_id: int, payload: UserDetailsUpdate,
):
    target_user = _get_user_or_404(db, user_id)
    _check_can_access_details(current_user, target_user)

    details = (
        db.query(models.UserDetails)
        .filter(models.UserDetails.user_id == user_id)
        .first()
    )
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User details not found",
        )
    #exclude_unset=True only provided fields are updated
    data = payload.model_dump(exclude_unset=True)
    db.query(models.UserDetails).filter(models.UserDetails.user_id == user_id).update(data)
    db.commit()



