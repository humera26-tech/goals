from sqlalchemy.orm import Session
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from database.models import Project, User
from schemas.project import ProjectCreate, ProjectUpdate


# CREATE
def create_project_service(db: Session, project_data: ProjectCreate, current_user: User):
    try:
        db_project = Project(
            project_name=project_data.name,
            description=project_data.description,
            project_type=project_data.project_type,
            client_id=project_data.client_id,
            billable_flag=project_data.billable_flag,
            internal_project_flag=project_data.internal_project_flag,
            created_at=project_data.created_at,
            status=project_data.status,
            user_id=project_data.user_id,
            org_id=project_data.org_id
            
        )
        
        db.add(db_project)
        db.commit()
        
        db.refresh(db_project)
        return db_project
    except SQLAlchemyError as e:
        print("Error creating project")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create project {e}")
    


def update_project(db: Session, project_id: int, project_data: ProjectUpdate):
    try:
        db_project = db.query(project).filter(project.project_id == project_id).first()
        
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db_project.project_name = project_data.name
        db_project.description = project_data.description
        db_project.status = project_data.status
        db.commit()
        db.refresh(db_project)
        
        return db_project
    except SQLAlchemyError as e:
        
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update project")


def delete_project(db: Session, project_id: int):
    try:
        db_project = db.query(project).filter(project.project_id == project_id).first()
        if not db_project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        db.delete(db_project)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete project")


# GET ALL PROJECTS
def get_all_projects(db: Session):
    try:
        projects = db.query(project).all()
        return projects
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to fetch projects")