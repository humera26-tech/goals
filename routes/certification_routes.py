from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from database.models import Certification
from database.database import SessionLocal
from schemas.certification import CertificationCreate,CertificationResponse, CertificationUpdate
from services.auth_service import get_current_user
from database import models
from database.database import get_db
from schemas.message import CertificationCreateResponse, CertificationUpdateResponse
from services.certification_service import create_certification_service,update_certification_service

router = APIRouter(tags=["Certification"])
# router = APIRouter(prefix="/certification", tags=["Certification"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create certification
@router.post("/", 
             response_model=CertificationCreateResponse,
             status_code=status.HTTP_201_CREATED)
def create_certification(data:CertificationCreate, db: Session = Depends(get_db),
                         user: models.User = Depends(get_current_user)):
  data = create_certification_service(db=db, current_user=user, payload=data)
  return CertificationCreateResponse(
      message="Certification created successfully",
      data=data,
  )



# Get all certifications for logged-in user
@router.get("/", response_model=list[CertificationResponse])
def get_all_certifications(db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    certs = db.query(Certification).filter(Certification.user_id == user.id).all()
    return certs


# Get certification by ID
@router.get("/{cert_id}", response_model=CertificationResponse)
def get_certification(cert_id: int,  db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):

    cert = db.query(Certification).filter(
        Certification.id == cert_id,
        Certification.user_id == user.id
    ).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")

    return cert


# Update certification

@router.put("/{cert_id}", response_model=CertificationUpdateResponse)
def update_certification(
    cert_id: int,
    data: CertificationUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),):

    cert = update_certification_service(
        db=db,
        current_user=user,
        cert_id=cert_id,
        payload=data,
    )
    #return {'message':'your certificate has been updated',"data_cert":cert}
    return CertificationUpdateResponse(
        message="Certification updated successfully",
        data=cert,
    )


# Delete certification
@router.delete("/{cert_id}")
def delete_certification(cert_id: int, 
 db: Session = Depends(get_db),
 user: models.User = Depends(get_current_user)):

    cert = db.query(Certification).filter(
        Certification.id == cert_id,
        Certification.user_id == user.id
    ).first()

    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")

    db.delete(cert)
    db.commit()

    return {"message": "Certification deleted successfully"}
          