from database.models import Certification
from fastapi import HTTPException
from schemas.certification import CertificationUpdate
from sqlalchemy.orm import Session

def create_certification_service(db, current_user, payload=None):
    new_cert = Certification(
        user_id=current_user.id,
        name=payload.name,
        provider=payload.provider,
        status=payload.status,
        planned_date=payload.planned_date,
        completed_date=payload.completed_date,
        expiry_date=payload.expiry_date,
    )
    db.add(new_cert)
    db.commit()
    db.refresh(new_cert)
    return new_cert

# def update_certification_service(db, current_user, payload=CertificationUpdate):
#     cert = db.query(Certification).filter(Certification.user_id == current_user.id, Certification.id == payload.id).first()
#     if not cert:
#         raise HTTPException(status_code=404, detail="Certification not found")
#     cert.name = payload.name
#     cert.provider = payload.provider
#     cert.status = payload.status
#     cert.planned_date = payload.planned_date
#     cert.completed_date = payload.completed_date
#     cert.expiry_date = payload.expiry_date
#     db.commit()
#     db.refresh(cert)
#     return cert

   

def update_certification_service(db, current_user, cert_id: int, payload=None):
    """
    Partially update a certification for the current user.

    Only fields actually provided in the payload will be updated.
    """
    cert = (
        db.query(Certification).filter(
            Certification.user_id == current_user.id,
            Certification.id == cert_id,
        )
        .first()
    )

    if not cert:
        raise HTTPException(status_code=404, detail="Certification not found")

    # Assume payload is a Pydantic model (e.g., CertificationUpdate)
    # Use exclude_unset so only provided fields are updated.
    if hasattr(payload, "model_dump"):
        update_data = payload.model_dump(exclude_unset=True)
    else:
        update_data = payload.dict(exclude_unset=True)

    for field, value in update_data.items():
        # Safety: only set attributes that actually exist on the model
        if hasattr(cert, field):
            setattr(cert, field, value)

    db.commit()
    db.refresh(cert)
    return cert