from database.models import Goals
from sqlalchemy.orm import Session
from schemas.goals import Goal_Create, Goal_Update, Goal_Response
from typing import List, Optional   
from database import models
from datetime import datetime
from services.permission import is_hr_manager,is_admin
from fastapi.responses import JSONResponse

def create_goal_services(db:Session,goal:Goal_Create,user_id:int):
    print(is_admin(user_id,db))
    if is_admin(user_id,db) :
        new_goal=models.Goals(title=goal.title,
            description=goal.description,
            goal_type=goal.goal_type,
            start_date=goal.start_date,
            end_date=goal.end_date,  
            status=goal.status,
            progress=goal.progress,
            created_at=datetime.now(),
            user_id=user_id
            )
        
        db.add(new_goal)
        db.commit()
        db.refresh(new_goal)
        return JSONResponse(content={"message": "Goal created successfully"})
    return JSONResponse(content={"message": "Invalid creditical"})
    


def form_goals_service():
    goals ={
        "goal_types": ["Individual", "Team"],
        "statuses": ["Pending", "In Progress", "Completed"]
    }
    return goals

def get_goals_service(db: Session, user_id: int):

    goals=db.query(models.Goals.title,
            models.Goals.description,
            models.Goals.end_date,
            models.Goals.progress,
            models.Goals.goal_type
            ).filter(models.Goals.user_id == user_id).all()
    
    return [
        {
            "title": goal.title,
            "description": goal.description,
            "end_date": goal.end_date,
            "progress": goal.progress,
            "goal_type": goal.goal_type,
    
        }
        for goal in goals
    ] 
    # return goals if goals else []  # Return an empty list if no goals are found

def get_goal_by_id_service(db:Session,goal_id:int,user_id:int)-> Optional[Goal_Response]:
    goal=db.query(models.Goals.title,
                  models.Goals.description,
                  models.Goals.end_date,
                  models.Goals.progress,
                  models.Goals.goal_type       
                  ).filter(models.Goals.id==goal_id,models.Goals.user_id==user_id).first()
    return {
            "title": goal.title, "description": goal.description,
            "end_date": goal.end_date,
            "progress": goal.progress,
            "goal_type": goal.goal_type,
    
        } if goal else None  # type: ignore

     

def update_goal_services(db:Session,goal_id:int,goal_update:Goal_Update,user_id:int)-> Optional[Goal_Response]:
    goal=db.query(models.Goals).filter(models.Goals.id==goal_id,models.Goals.user_id==user_id).first()
    if not goal:
        return None
    for var, value in vars(goal_update).items():
        if value is not None:
            setattr(goal, var, value)
    db.commit()
    db.refresh(goal)
    return goal 


def delete_goal(db:Session,goal_id:int,user_id:int)-> bool:
    goal=db.query(models.Goals).filter(models.Goals.id==goal_id,models.Goals.user_id==user_id).first()
    if not goal:
        return False
    db.delete(goal)
    db.commit()
    return True

