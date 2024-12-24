from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.models.models import Organization
from app.schemas.organizations.contact_schema import ContactSchema

router = APIRouter()

@router.get("/organizations/{org_id}/contact", response_model=ContactSchema)
def get_contact(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org.contact

@router.get("/organizations/{org_id}/contact/{contact_id}", response_model=ContactSchema)
def get_contact_by_id(org_id: int, contact_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    if org.contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return org.contact

@router.patch("/organizations/{org_id}/contact", response_model=ContactSchema)
def update_contact(org_id: int, contact: ContactSchema, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    org.contact = contact
    db.commit()
    db.refresh(org)
    return org.contact

@router.post("/organizations/{org_id}/contact", response_model=ContactSchema)
def create_contact(org_id: int, contact: ContactSchema, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    org.contact = contact
    db.commit()
    db.refresh(org)
    return org.contact

@router.delete("/organizations/{org_id}/contact", response_model=ContactSchema)
def delete_contact(org_id: int, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if org is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    contact = org.contact
    org.contact = None
    db.commit()
    return contact