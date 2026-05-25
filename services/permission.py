from database import models
from sqlalchemy.orm import Session

def is_hr_manager(user_id: int, db: Session) -> bool:
    rolename = db.query(models.User.role_id).filter(models.User.id == user_id).first()
    
    role=db.query(models.Role.role_name).filter(models.Role.id==rolename.role_id).scalar()
    print(f"User ID: {user_id}, Role ID: {rolename}, Role Name: {role}")
    return role == "HR"

def is_admin(user_id: int, db: Session) -> bool:
    role_id = db.query(models.User.role_id).filter(models.User.id == user_id).first()
    role=db.query(models.Role.role_name).filter(models.Role.id==role_id.role_id).scalar()
    return role.lower() == "admin"

def is_manager(user_id: int, db: Session) -> bool:
    role_id = db.query(models.User.role_id).filter(models.User.id == user_id).first()
    role=db.query(models.Role.role_name).filter(models.Role.id==role_id.role_id).scalar()
    return role == "Manager"

