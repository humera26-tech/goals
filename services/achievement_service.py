from sqlalchemy.orm import Session
from database import models
from schemas.achievement import AchievementCreate, AchievementOut

# Create an achievement for user
def create_achievement_for_user(
    db: Session,
    current_user: models.User,
    payload: AchievementCreate,
) -> AchievementOut:

    achievement = models.Achievement(
        user_id=current_user.id,
        awarded_by_id=payload.awarded_by_id,
        title=payload.title,
        description=payload.description,
        awarded_date=payload.awarded_date,
    )

    db.add(achievement)
    db.commit()
    db.refresh(achievement)

    return AchievementOut.from_orm(achievement)


def list_achievements_for_user(
    db: Session,
    user_id: int,
) -> list[AchievementOut]:
    achievements = (
        db.query(models.Achievement)
        .filter(models.Achievement.user_id == user_id)
        .order_by(models.Achievement.awarded_date.desc())
        .all()
    )

    return achievements

