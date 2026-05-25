from database import models
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db


from schemas.performance_review import (
    PerformanceReviewCreate,
    PerformanceReviewResponse,
    PerformanceReviewUpdate
)
from services.peformance_services import performance_review_service

router = APIRouter(prefix="/reviews", tags=["Performance Reviews"])


@router.post("/", response_model=PerformanceReviewResponse)
def create_review(review: PerformanceReviewCreate, db: Session = Depends(get_db)):
    return performance_review_service.create_review(db, review)





@router.get("/", response_model=List[PerformanceReviewResponse])
def get_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return performance_review_service.get_reviews(db, skip,limit)







@router.get("/{review_id}", response_model=PerformanceReviewResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = performance_review_service.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.put("/{review_id}", response_model=PerformanceReviewResponse)
def update_review(review_id: int, review: PerformanceReviewUpdate, db: Session = Depends(get_db)):
    updated = performance_review_service.update_review(db, review_id, review)
    if not updated:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    deleted = performance_review_service.delete_review(db, review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}

@router.get("/user/{user_id}", response_model=List[PerformanceReviewResponse])
def get_reviews_for_user(user_id: int, db: Session = Depends(get_db)):
    review = db.query(models.PerformanceReview).filter(models.PerformanceReview. user_id==user_id).all()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review