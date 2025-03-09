import logging

from fastapi import APIRouter, Depends, HTTPException
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.models import Organization
from root.root_elements import router
from schemas.schemas import OrganizationSchema


@router.get("/{client_id}/organizations", response_model=List[OrganizationSchema])
async def read_organizations(client_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    logging.info(f"Fetching organizations for client_id: {client_id}")
    organizations = db.query(Organization).filter(Organization.client_id == client_id).offset(skip).limit(limit).all()
    return organizations

@router.post("/{client_id}/organizations", response_model=OrganizationSchema)
async def create_organization(client_id: int, organization: OrganizationSchema, db: Session = Depends(get_db)):
    logging.info(f"Received organization data for client_id {client_id}: {jsonable_encoder(organization)}")
    try:
        db_organization = Organization(**organization.dict(), client_id=client_id)
        db.add(db_organization)
        db.commit()
        db.refresh(db_organization)
        return db_organization
    except Exception as e:
        logging.error(f"Error creating organization: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{client_id}/organizations/{organization_id}", response_model=OrganizationSchema)
async def update_organization(client_id: int, organization_id: int, organization: OrganizationSchema, db: Session = Depends(get_db)):
    db_organization = db.query(Organization).filter(Organization.id == organization_id, Organization.client_id == client_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    update_data = organization.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_organization, key, value)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@router.delete("/{client_id}/organizations/{organization_id}", response_model=OrganizationSchema)
async def delete_organization(client_id: int, organization_id: int, db: Session = Depends(get_db)):
    db_organization = db.query(Organization).filter(Organization.id == organization_id, Organization.client_id == client_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(db_organization)
    db.commit()
    return db_organization


