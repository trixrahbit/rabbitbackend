from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from api.user.user_router import get_db
from models.models import Organization, Contact
from root.root_elements import router
from schemas.organizations.contact_schema import ContactSchema, ContactCreate, ContactUpdate
from typing import List

# GET ALL CONTACTS FOR AN ORGANIZATION
@router.get("/organizations/{org_id}/contacts", response_model=List[ContactSchema])
def get_contacts(org_id: int, db: Session = Depends(get_db)):
    contacts = db.query(Contact).filter(Contact.organization_id == org_id).all()
    if not contacts:
        raise HTTPException(status_code=404, detail="No contacts found for this organization")
    return contacts

# GET A SPECIFIC CONTACT
@router.get("/organizations/{org_id}/contacts/{contact_id}", response_model=ContactSchema)
def get_contact_by_id(org_id: int, contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.organization_id == org_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

# CREATE A NEW CONTACT
@router.post("/organizations/{org_id}/contacts", response_model=ContactSchema)
def create_contact(org_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    new_contact = Contact(**contact.dict(), organization_id=org_id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# UPDATE A CONTACT
@router.patch("/organizations/{org_id}/contacts/{contact_id}", response_model=ContactSchema)
def update_contact(org_id: int, contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.organization_id == org_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    update_data = contact_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact

# DELETE A CONTACT
@router.delete("/organizations/{org_id}/contacts/{contact_id}", response_model=ContactSchema)
def delete_contact(org_id: int, contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.organization_id == org_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return contact
