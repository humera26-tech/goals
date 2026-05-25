from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.feedback import Feedback_Create
from services.feedback_service import feedback_form_service, create_feedback_service
from services.auth_service import get_current_user
import database.models as models

router = APIRouter(prefix="/feedback", tags=["Feedback"])

@router.get("/feedbacks_form")
def get_feedbacks_form(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):

    feedback_form = feedback_form_service(db)
    return feedback_form

@router.post("/")
def create_feedback(feedback: Feedback_Create, db: Session = Depends(get_db),           current_user: models.User = Depends(get_current_user)):
    # Implement the logic to create feedback in the database
    # For example, you can use SQLAlchemy to add a new feedback record
    
    new_feedback = create_feedback_service(db, feedback, current_user.id) 
    
    return new_feedback