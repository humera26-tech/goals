
# Create
@router.post("/", response_model=Feedback_Create)
def create(payload:Feedback_Create, db: Session = Depends(get_db),user_id: int = Depends(get_current_user)):
    return feedback_service(db, payload,user_id)

# Get all
@router.get("/", response_model=list[FeedbackResponse])
def get_all(db: Session = Depends(get_db)):
    return feedback_service.get_all_feedback(db)

# Get by ID
@router.get("/{feedback_id}", response_model=FeedbackResponse)
def get_one(feedback_id: int, db: Session = Depends(get_db)):
    feedback = feedback_service.get_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

# Update
@router.put("/{feedback_id}", response_model=FeedbackResponse)
def update(feedback_id: int, payload: FeedbackUpdate, db: Session = Depends(get_db)):
    feedback = feedback_service.update_feedback(db, feedback_id, payload)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback

# Delete
@router.delete("/{feedback_id}")
def delete(feedback_id: int, db: Session = Depends(get_db)):
    feedback = feedback_service.delete_feedback(db, feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return {"message": "Feedback deleted successfully"}