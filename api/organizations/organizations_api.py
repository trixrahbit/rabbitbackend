import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.user.user_router import get_db
from auth.auth_util import get_current_user
from models.models import Organization, User
from root.root_elements import router
from schemas.schemas import OrganizationSchema

# Configure logging
logger = logging.getLogger(__name__)


@router.get("/organizations", response_model=List[OrganizationSchema])
async def get_organizations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch organizations based on user role."""

    if current_user.is_superuser:
        # Super Admin: See all organizations
        organizations = db.query(Organization).all()
    else:
        # Regular User: See only their organization
        organizations = db.query(Organization).filter(Organization.id == current_user.organization_id).all()

    return organizations


@router.patch("/organizations/{org_id}", response_model=OrganizationSchema)
async def update_organization(org_id: int, organization: OrganizationSchema, db: Session = Depends(get_db)):
    db_organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    update_data = organization.model_dump(exclude_unset=True)  # ✅ Fix for Pydantic v2
    for key, value in update_data.items():
        setattr(db_organization, key, value)

    db.commit()
    db.refresh(db_organization)
    return db_organization


@router.delete("/organizations/{org_id}", response_model=OrganizationSchema)
async def delete_organization(org_id: int, db: Session = Depends(get_db)):
    organization = db.query(Organization).filter(Organization.org_id == org_id).first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(organization)
    db.commit()
    return organization

@router.post("/organizations", response_model=OrganizationSchema)
async def create_organization(organization: OrganizationSchema, db: Session = Depends(get_db)):
    new_organization = Organization(**organization.model_dump())  # ✅ Using model_dump() for Pydantic v2
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization
