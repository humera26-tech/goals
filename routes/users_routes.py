from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from services.user_service import get_basic_details_user_service, change_password_service, create_user_in_org_service, \
    update_user_details
from services.auth_service import get_current_user
from services.user_service import (
    create_user_details,
    get_user_details,
    
)
from services.education_service import (
    add_education_for_user,
    list_education_for_user,
    update_education_for_user,
    delete_education_for_user,
)
from services.achievement_service import (create_achievement_for_user,
                                          list_achievements_for_user)
from schemas.achievement import AchievementCreate, AchievementOut
from schemas.message import MessageResponse
from schemas.user import UserBasicOut, ChangePasswordRequest, UserCreateInOrg
from schemas.user import (
    UserDetailsCreate,
    UserDetailsUpdate,
    UserDetailsOut,
)
from schemas.education import EducationCreate, EducationUpdate, EducationOut

router = APIRouter(tags=["User"])


@router.get("/profile", status_code=status.HTTP_200_OK)
def get_basic_details_user(
        current_user=Depends(get_current_user),
):
    return get_basic_details_user_service(current_user)


@router.post("/change-password", response_model=MessageResponse)
def change_password(
        payload: ChangePasswordRequest,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    change_password_service(db=db, current_user=current_user, payload=payload)
    return MessageResponse(message="Password updated successfully")


@router.post("/", status_code=status.HTTP_201_CREATED, )
def add_user_to_org(payload: UserCreateInOrg, db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user), ):
    create_user_in_org_service(db=db, current_user=current_user, payload=payload, )
    return MessageResponse(message="User added successfully in your organization")


@router.post("/{user_id}/details", status_code=status.HTTP_201_CREATED, )
def create_details_for_user(
        user_id: int,
        payload: UserDetailsCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    create_user_details(
        db=db, current_user=current_user,
        user_id=user_id, payload=payload,
    )

    return MessageResponse(message="User Details added sucessfully")


@router.get("/{user_id}/details", response_model=UserDetailsOut,
            status_code=status.HTTP_200_OK, )
def get_details_for_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    return get_user_details(
        db=db,
        current_user=current_user,
        user_id=user_id,
    )


@router.put("/{user_id}/details", status_code=status.HTTP_200_OK, )
def update_details_for_user(
        user_id: int, payload: UserDetailsUpdate,
        db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user),
):
    update_user_details(
        db=db,
        current_user=current_user,
        user_id=user_id,
        payload=payload,
    )

    return MessageResponse(message="User Details Updated successfully")


# Add education (UG / PG / Other)
@router.post(
    "/{user_id}/education",
    status_code=status.HTTP_201_CREATED,
)
def add_education(
        user_id: int,
        payload: EducationCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    print("jj")
    print(payload)
    add_education_for_user(db, current_user, user_id, payload)
    return MessageResponse(message="Education details added successfully")


# get user's education details
@router.get("/education", response_model=list[EducationOut])
def get_my_education(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    educations = list_education_for_user(db, current_user, current_user.id)

    return educations


# update specific education record
@router.put(
    "/{user_id}/education/{education_id}",
    status_code=status.HTTP_200_OK,
)
def update_education(
        user_id: int,
        education_id: int,
        payload: EducationUpdate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    update_education_for_user(
        db=db,
        current_user=current_user,
        user_id=user_id,
        education_id=education_id,
        payload=payload,
    )

    return MessageResponse(message="education details updated successfully")


# Delete a specific education record
@router.delete(
    "/{user_id}/education/{education_id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
def delete_education(
        user_id: int,
        education_id: int,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user),
):
    delete_education_for_user(
        db=db,
        current_user=current_user,
        user_id=user_id,
        education_id=education_id,
    )
    return MessageResponse(message="Education record deleted successfully")


# add new achievement for user
@router.post("/achievement", status_code=status.HTTP_201_CREATED)
def add_my_achievement(
        payload: AchievementCreate,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user), ):
    create_achievement_for_user(db=db, current_user=current_user, payload=payload)
    return MessageResponse(message="Achievement added successfully")

# get achievement of user
@router.get("/achievement", response_model=list[AchievementOut], status_code=status.HTTP_200_OK, )
def get_my_achievements(
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user), ):

    user_achievement = list_achievements_for_user(db, current_user.id)
    return user_achievement
