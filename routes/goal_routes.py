from ast import List

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from services.auth_service import get_current_user
from services.goals_service import create_goal_services, get_goals_service, get_goal_by_id_service, update_goal_services, form_goals_service
from schemas.goals import Goal_Create, Goal_Response,Goal_Update
from database import models

router = APIRouter(prefix="/goals", tags=["goals"])

@router.post("/", response_model=Goal_Create, status_code=status.HTTP_201_CREATED)
def create_goal(goal: Goal_Create, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    new_goal = create_goal_services(db, goal, current_user.id)       
    
    return new_goal
    # return (status_code=status.HTTP_201_CREATED, content={"message": "Goal created successfully", "goal": new_goal})

@router.get("/form-data")
def form_goals():
    goals = form_goals_service()
    
    return goals

@router.get("/")
def fetch_goals(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    goals = get_goals_service(db, current_user.id)
    return goals





@router.get("/{goal_id}")
def get_goal_by_id(goal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    goal = get_goal_by_id_service(db, goal_id, current_user.id)
    return goal     

@router.put("/{goal_id}",response_model=Goal_Update)
def update_goal(goal_id: int, goal_update: Goal_Update, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    goal=update_goal_services(db,goal_id,goal_update,current_user.id)
      
    return goal
    # goal = db.query(models.Goals).filter(models.Goals.id == goal_id, models.Goals.user_id == current_user.id).first()
    # if not goal:
    #     return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Goal not found"})
    # for var, value in vars(goal_update).items():
    #     if value is not None:
    #         setattr(goal, var, value)
    # db.commit()
    # db.refresh(goal)
         

@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)        
def delete_goal(goal_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    goal = db.query(models.Goals).filter(models.Goals.id == goal_id, models.Goals.user_id == current_user.id).first()
    if not goal:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"message": "Goal not found"})
    db.delete(goal)
    db.commit()
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={"message": "Goal deleted successfully"})

