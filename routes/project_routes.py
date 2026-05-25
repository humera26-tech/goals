from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from services.auth_service import get_current_user
from schemas.project import ProjectCreate, ProjectResponse, ProjectListResponse, ProjectUpdate
from schemas.message import ProjectCreateResponse, ProjectUpdateResponse
from services.project_service import create_project_service, update_project, delete_project as delete_project_service, get_all_projects

router = APIRouter(prefix="", tags=["Projects"])


@router.post("/", response_model=ProjectCreateResponse)
def create_project_api(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
      # kept for auth, not passed to service
    
    create_project_service(db, payload,current_user)
    # return ProjectCreateResponse(message="Project created successfully", data=project)
    

@router.put("/{id}", response_model=ProjectUpdateResponse)
def update_project_api(
    id: int,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    project = update_project(db, id, payload)
    if not project:
        raise HTTPException(status_code=403, detail="Not authorized to update project")
    return ProjectUpdateResponse(message="Project updated successfully", data=project)


@router.delete("/{id}")
def delete_project_api(
    id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    success = delete_project_service(db, id, user)
    if not success:
        raise HTTPException(status_code=403, detail="Not authorized to delete project")
    return {"message": "Project deleted successfully"}


