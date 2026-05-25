from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from database import models
from schemas.auth import LoginRequest, TokenResponse
from schemas.message import MessageResponse
from utils import verify_password
from services.auth_service import verify_password, create_access_token, get_current_user
import uuid


router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    # Always compare email in lowercase for consistency
    email = data.email.lower()

    # Find user by work_email
    user = db.query(models.User).filter(models.User.work_email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    # Verify hashed password
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    # Generate a new session id for this login
    new_session_id = str(uuid.uuid4())
    user.session_id = new_session_id
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create JWT
    access_token = create_access_token({
        "sub": str(user.id),
        "sid": new_session_id,
    })
    return TokenResponse(access_token=access_token)

@router.post("/logout", response_model=MessageResponse)
def logout(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    current_user.session_id = None
    db.add(current_user)
    db.commit()

    return MessageResponse(message="Logged out successfully")
