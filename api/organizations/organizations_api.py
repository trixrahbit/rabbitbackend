from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session

from db_config.db_connection import get_db
from auth.auth_util import get_current_user
from models.models import Organization, User
from models.organizationModels.orgModel import OrganizationType, Industry, OrganizationSize
from root.root_elements import router
from schemas.organizations.organization_schema import OrganizationTypeSchema, IndustrySchema, OrganizationSizeSchema
from schemas.schemas import OrganizationSchema
from logger_config import logger



# Helper function to check if user is a super admin
def require_super_admin(user: dict):
    if not user.get("super_admin", False):
        logger.warning("❌ Unauthorized access attempt by non-super admin.")
        raise HTTPException(status_code=403, detail="Super Admin access required")

# 🔹 GET Organizations (Only show all if Super Admin)
@router.get("/organizations", response_model=List[OrganizationSchema])
async def get_organizations(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Fetch organizations based on user role."""
    logger.debug(f"🟢 User {current_user.email} requesting organizations. Super Admin: {current_user.super_admin}")

    if current_user.super_admin:
        organizations = db.query(Organization).all()
        logger.info(f"✅ Retrieved {len(organizations)} organizations for Super Admin.")
    else:
        organizations = db.query(Organization).filter(Organization.id == current_user.organization_id).all()
        logger.warning(f"⚠️ Non-admin user {current_user.email} accessing organization {current_user.organization_id}")

    return organizations

# 🔹 POST: Update Organization
from fastapi import Header

@router.post("/organizations/{org_id}", response_model=OrganizationSchema)
async def update_organization(
    org_id: int,
    organization: OrganizationSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    super_admin_org_id: int = Header(None),  # ✅ Get logged-in user's org ID from header
):
    logger.info(f"🔄 Attempting to update organization {org_id} via POST")

    # ✅ Ensure the logged-in user's org ID is provided
    if not super_admin_org_id:
        logger.error(f"❌ Missing Super Admin Org ID in request headers")
        raise HTTPException(status_code=400, detail="Super Admin Org ID is required")

    # ✅ Check if the logged-in user is a super admin OR if they belong to the specified org
    if not (current_user.super_admin or super_admin_org_id == org_id):
        logger.error(f"❌ Unauthorized update attempt by {current_user.get('email')} on org {org_id}")
        raise HTTPException(status_code=403, detail="Not authorized to update this organization")

    # ✅ Fetch the organization that needs updating
    db_organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not db_organization:
        logger.error(f"❌ Organization {org_id} not found")
        raise HTTPException(status_code=404, detail="Organization not found")

    try:
        update_data = organization.model_dump(exclude_unset=True)
        logger.debug(f"📝 Incoming update data: {update_data}")

        for key, value in update_data.items():
            setattr(db_organization, key, value)

        db.commit()
        db.refresh(db_organization)
        logger.info(f"✅ Organization {org_id} updated successfully via POST.")
        return db_organization

    except Exception as e:
        logger.error(f"⚠️ Server Error while updating {org_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")




# 🔹 DELETE Organization (Super Admin Required)
@router.delete("/organizations/{org_id}", response_model=OrganizationSchema)
async def delete_organization(
    org_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_super_admin(current_user)

    organization = db.query(Organization).filter(Organization.id == org_id).first()
    if not organization:
        logger.error(f"❌ Organization {org_id} not found for deletion.")
        raise HTTPException(status_code=404, detail="Organization not found")

    db.delete(organization)
    db.commit()
    logger.info(f"🗑️ Organization {org_id} deleted successfully.")
    return organization

# 🔹 CREATE Organization (Super Admin Required)
@router.post("/organizations", response_model=OrganizationSchema)
async def create_organization(
    organization: OrganizationSchema,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    require_super_admin(current_user)

    new_organization = Organization(**organization.model_dump())
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)
    logger.info(f"🎉 New organization created with ID {new_organization.id}.")
    return new_organization

# 🔹 GET Organization Types
@router.get("/org_types", response_model=List[OrganizationTypeSchema])
async def get_organization_types(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.debug("Fetching organization types...")
    return db.query(OrganizationType).all()

# 🔹 GET Industries
@router.get("/industries", response_model=List[IndustrySchema])
async def get_industries(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.debug("Fetching industries...")
    return db.query(Industry).all()

# 🔹 GET Organization Sizes
@router.get("/org_sizes", response_model=List[OrganizationSizeSchema])
async def get_organization_sizes(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    logger.debug("Fetching organization sizes...")
    return db.query(OrganizationSize).all()
