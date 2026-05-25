import re
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database.database import get_db
from schemas.organization import OrgWithUserCreate
from services.organization_service import register_org_with_user_service
from schemas.message import MessageResponse

router = APIRouter(tags=["Organization"])

# Registering new organization with the user
@router.post("/onboard-organization",  status_code=status.HTTP_201_CREATED)
def register_org_with_user(
    payload: OrgWithUserCreate,
    db: Session = Depends(get_db),
):

    register_org_with_user_service(db=db, payload=payload)
    return MessageResponse(message="Organization created successfully")

 