
from database.models import Feedback
from database import models

# def feedback_service(db, payload,user_id):
#     # Implement the logic to create feedback in the database
#     # For example, you can use SQLAlchemy to add a new feedback record
#     new_feedback = Feedback(
#         user_id=payload.user_id,
#         given_by=user_id, # manager or peer who is giving the feedback
#         feedback_type=payload.feedback_type,
#         comment=payload.comment,
#         rating=payload.rating,
#         created_at=payload.created_at
#     )
#     db.add(new_feedback)
#     db.commit()
#     db.refresh(new_feedback)
#     return new_feedback

def feedback_form_service(db):
    # Implement the logic to retrieve feedback form details
    # This could include feedback types, rating scales, etc.
    rname=db.query(models.User).all()
    feedback_form = {
        "recipients_name": [user.username for user in rname],
        "feedback_types": ["peer", "manager", "direct report","client"],
        "rating_scale": [1, 2, 3, 4, 5]
    }
    return feedback_form

def create_feedback_service(db, feedback, current_user_id):
    review_id=db.query(models.User.id).filter(models.User.username == feedback.reviewer_name).scalar()
    print("Review id :",review_id)
    new_feedback = models.PerformanceReview(
        user_id=current_user_id,
        reviewer_id=review_id, # manager or peer who is giving the feedback
        review_period=feedback.review_period,
        overall_rating=feedback.overall_rating,
        strengths=feedback.strengths,
        improvements=feedback.improvement,
        created_at=feedback.created_at
    )
    db.add(new_feedback)
    db.commit()
    db.refresh(new_feedback)
    return new_feedback
