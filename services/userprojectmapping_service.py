from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models import UserProjectMapping
from schemas.userprojectmapping import (
    UserProjectMappingCreate,
    UserProjectMappingUpdate
)


class UserProjectMappingService:

    @staticmethod
    def create(db: Session, payload: UserProjectMappingCreate):
        obj = UserProjectMapping(**payload.model_dump())
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def get_by_id(db: Session, mapping_id: int):
        obj = db.query(UserProjectMapping).filter(
            UserProjectMapping.id == mapping_id
        ).first()

        if not obj:
            raise HTTPException(status_code=404, detail="Mapping not found")

        return obj

    @staticmethod
    def get_all(db: Session):
        return db.query(UserProjectMapping).all()

    @staticmethod
    def update(db: Session, mapping_id: int, payload: UserProjectMappingUpdate):
        obj = UserProjectMappingService.get_by_id(db, mapping_id)

        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)

        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, mapping_id: int):
        obj = UserProjectMappingService.get_by_id(db, mapping_id)

        db.delete(obj)
        db.commit()

        return {"message": "Mapping deleted successfully"}
    
    