import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.user.user_router import get_db
from auth.auth_util import get_current_user
from models.models import Organization, User
from models.organizationModels.orgModel import OrganizationType, Industry, OrganizationSize
from root.root_elements import router
from schemas.organizations.organization_schema import OrganizationTypeSchema, IndustrySchema, OrganizationSizeSchema
from schemas.schemas import OrganizationSchema

# Configure logging
logger = logging.getLogger(__name__)

# Helper function to check if user is a super admin
def require_super_admin(user: dict):
    if not user.get("super_admin", False):  # ✅ Check super_admin status
        raise HTTPException(status_code=403, detail="Super Admin access required")

# 🔹 GET Organizations (Only show all if Super Admin)
@router.get("/organizations", response_model=List[OrganizationSchema])
async def get_organizations(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """Fetch organizations based on user role."""

    logger.info(f"User {current_user['email']} requesting organizations. Super Admin: {current_user.get('super_admin', False)}")

    if current_user.get("super_admin", False):  # ✅ Super Admins see all
        organizations = db.query(Organization).all()
    else:
        organizations = db.query(Organization).filter(Organization.id == current_user["organization_id"]).all()

    return organizations

# 🔹 UPDATE Organization (Super Admin Required)
@router.patch("/organizations/{org_id}", response_model=OrganizationSchema)
async def update_organization(
    org_id: int,
    organization: OrganizationSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_super_admin(current_user)  # ✅ Enforce Super Admin

    db_organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not db_organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    update_data = organization.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_organization, key, value)

    db.commit()
    db.refresh(db_organization)
    return db_organization

# 🔹 DELETE Organization (Super Admin Required)
@router.delete("/organizations/{org_id}", response_model=OrganizationSchema)
async def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_super_admin(current_user)  # ✅ Enforce Super Admin

    organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")

    db.delete(organization)
    db.commit()
    return organization

# 🔹 CREATE Organization (Super Admin Required)
@router.post("/organizations", response_model=OrganizationSchema)
async def create_organization(
    organization: OrganizationSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_super_admin(current_user)  # ✅ Enforce Super Admin

    new_organization = Organization(**organization.model_dump())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    return new_organization

# 🔹 GET Organization Types (No Super Admin Required)
@router.get("/org_types", response_model=List[OrganizationTypeSchema])
async def get_organization_types(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(OrganizationType).all()

# 🔹 GET Industries (No Super Admin Required)
@router.get("/industries", response_model=List[IndustrySchema])
async def get_industries(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(Industry).all()

# 🔹 GET Organization Sizes (No Super Admin Required)
@router.get("/org_sizes", response_model=List[OrganizationSizeSchema])
async def get_organization_sizes(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    return db.query(OrganizationSize).all()
