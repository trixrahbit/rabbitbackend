from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from db_config.db_connection import get_db
from models import Contact
from models.models import Organization, Client
from root.root_elements import router
from schemas.client.contact_schema import ContactSchema, ContactUpdate, ContactCreate
from typing import List


# ✅ GET ALL CONTACTS FOR A CLIENT IN AN ORGANIZATION
@router.get("/organizations/{org_id}/clients/{client_id}/contacts", response_model=List[ContactSchema])
def get_contacts(org_id: int, client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found in this organization")

    contacts = db.query(Contact).filter(Contact.client_id == client_id).all()
    return contacts


# ✅ GET A SPECIFIC CONTACT
@router.get("/organizations/{org_id}/clients/{client_id}/contacts/{contact_id}", response_model=ContactSchema)
def get_contact_by_id(org_id: int, client_id: int, contact_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found in this organization")

    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.client_id == client_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


# ✅ CREATE A NEW CONTACT (Associates with Client in Organization)
@router.post("/organizations/{org_id}/clients/{client_id}/contacts", response_model=ContactSchema)
def create_contact(org_id: int, client_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found in this organization")

    contact_data = contact.dict(exclude={"client_id"})

    # ✅ Force conversion to string if needed
    contact_data["role"] = str(contact_data["role"]) if contact_data["role"] else None

    new_contact = Contact(**contact_data, client_id=client_id)
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact



# ✅ UPDATE A CONTACT
@router.patch("/organizations/{org_id}/clients/{client_id}/contacts/{contact_id}", response_model=ContactSchema)
def update_contact(org_id: int, client_id: int, contact_id: int, contact_update: ContactUpdate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found in this organization")

    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.client_id == client_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    update_data = contact_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(contact, key, value)

    db.commit()
    db.refresh(contact)
    return contact


# ✅ DELETE A CONTACT
@router.delete("/organizations/{org_id}/clients/{client_id}/contacts/{contact_id}", response_model=ContactSchema)
def delete_contact(org_id: int, client_id: int, contact_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found in this organization")

    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.client_id == client_id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")

    db.delete(contact)
    db.commit()
    return contact
