from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db  
from schemas.userprojectmapping import (
    UserProjectMappingCreate,
    UserProjectMappingUpdate,
    UserProjectMappingResponse
)
from services.userprojectmapping_service import UserProjectMappingService
from schemas.message import UserProjectMappingCreateResponse, UserProjectMappingUpdateResponse

from typing import List
from services.auth_service import get_current_user
from database import models


# `main.py` already mounts this router at `/api/user/userprojectmapping`.
# Keep routes clean so endpoints become:
#   POST   /api/user/userprojectmapping/
#   GET    /api/user/userprojectmapping/{mapping_id}
#   PUT    /api/user/userprojectmapping/{mapping_id}
#   DELETE /api/user/userprojectmapping/{mapping_id}
router = APIRouter(prefix="", tags=["User Project Mapping"])


@router.post("/", response_model=UserProjectMappingResponse)
def create_mapping(
    payload: UserProjectMappingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    payload_data = payload.model_dump()
    # Prevent users from creating mappings for other users.
    payload_data["user_id"] = current_user.id
    return UserProjectMappingService.create(db, UserProjectMappingCreate(**payload_data))


@router.get("/{mapping_id}", response_model=UserProjectMappingResponse)
def get_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    mapping = UserProjectMappingService.get_by_id(db, mapping_id)
    if int(mapping.user_id) != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return mapping


@router.get("/", response_model=List[UserProjectMappingResponse])
def get_all_mappings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    all_mappings = UserProjectMappingService.get_all(db)
    return [m for m in all_mappings if int(m.user_id) == int(current_user.id)]


@router.put("/{mapping_id}", response_model=UserProjectMappingResponse)
def update_mapping(
    mapping_id: int,
    payload: UserProjectMappingUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    mapping = UserProjectMappingService.get_by_id(db, mapping_id)
    if int(mapping.user_id) != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return UserProjectMappingService.update(db, mapping_id, payload)


@router.delete("/{mapping_id}")
def delete_mapping(
    mapping_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    mapping = UserProjectMappingService.get_by_id(db, mapping_id)
    if int(mapping.user_id) != int(current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return UserProjectMappingService.delete(db, mapping_id)

