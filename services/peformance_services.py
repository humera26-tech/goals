from sqlalchemy.orm import Session
from database import models
from database.models import PerformanceReview
from schemas.performance_review import PerformanceReviewCreate, PerformanceReviewUpdate



def create_review(db: Session, review: PerformanceReviewCreate):
    db_review = PerformanceReview(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(PerformanceReview).offset(skip).limit(limit).all()


def get_review_by_id(db: Session, review_id: int):
    return db.query(PerformanceReview).filter(PerformanceReview.id == review_id).first()


def update_review(db: Session, review_id: int, update_data: PerformanceReviewUpdate):
    review = get_review_by_id(db, review_id)
    if not review:
        return None

    for key, value in update_data.model_dump(exclude_unset=True).items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)
    return review 


return get_reviews(db)  
db.commit()
return review

    
    



def delete_review(db: Session, review_id: int):
    review = get_review_by_id(db, review_id)
    if not review:
        return None

    db.delete(review)
    db.commit()
    return review

