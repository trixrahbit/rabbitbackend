import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.models import Organization
from root.root_elements import router
from schemas.schemas import OrganizationSchema

# Configure logging
logger = logging.getLogger(__name__)


@router.get("/{org_id}", response_model=OrganizationSchema)
async def get_organization(org_id: int, db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.org_id == org_id).first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.patch("/{org_id}", response_model=OrganizationSchema)
async def update_organization(org_id: int, organization: OrganizationSchema, db: Session = Depends(get_db)):
    db_organization = db.query(Organization).filter(Organization.org_id == org_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    update_data = organization.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_organization, key, value)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@router.delete("/{org_id}", response_model=OrganizationSchema)
async def delete_organization(org_id: int, db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.org_id == org_id).first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(organization)
    db.commit()
    return organization

@router.post("/{org_id}", response_model=OrganizationSchema)
async def create_organization(org_id: int, organization: OrganizationSchema, db: Session = Depends(get_db)):
    organization = Organization(**organization.dict())
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization