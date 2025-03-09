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


@router.get("/{client_id}/organizations", response_model=List[OrganizationSchema])
async def read_organizations(client_id: int, db: Session = Depends(get_db)):
    organizations = (
        db.query(Organization)
        .filter(Organization.client_id == client_id)
        .order_by(Organization.id.asc())  # 🔥 Ensures MSSQL does not require OFFSET
        .all()  # ⚠️ Ensure this is `.all()` and NOT `.offset(...).limit(...)`
    )
    return organizations



@router.post("/{client_id}/organizations", response_model=OrganizationSchema)
async def create_organization(client_id: int, organization: OrganizationSchema, db: Session = Depends(get_db)):
    """Create a new organization for a specific client."""
    logger.info(f"Received organization data for client_id {client_id}: {jsonable_encoder(organization)}")

    try:
        db_organization = Organization(**organization.model_dump(), client_id=client_id)
        db.add(db_organization)
        db.commit()
        db.refresh(db_organization)

        logger.info(f"Created organization with ID {db_organization.id} for client {client_id}")
        return db_organization

    except Exception as e:
        logger.error(f"Error creating organization: {str(e)}")
        raise HTTPException(status_code=400, detail="Failed to create organization")


@router.patch("/{client_id}/organizations/{organization_id}", response_model=OrganizationSchema)
async def update_organization(client_id: int, organization_id: int, organization: OrganizationSchema,
                              db: Session = Depends(get_db)):
    """Update an existing organization."""
    db_organization = db.query(Organization).filter(
        Organization.id == organization_id, Organization.client_id == client_id
    ).first()

    if not db_organization:
        logger.warning(f"Organization ID {organization_id} not found for client {client_id}")
        raise HTTPException(status_code=404, detail="Organization not found")

    update_data = organization.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_organization, key, value)

    db.commit()
    db.refresh(db_organization)

    logger.info(f"Updated organization {organization_id} for client {client_id}")
    return db_organization


@router.delete("/{client_id}/organizations/{organization_id}", response_model=OrganizationSchema)
async def delete_organization(client_id: int, organization_id: int, db: Session = Depends(get_db)):
    """Delete an organization."""
    db_organization = db.query(Organization).filter(
        Organization.id == organization_id, Organization.client_id == client_id
    ).first()

    if not db_organization:
        logger.warning(f"Attempted to delete non-existing organization {organization_id} for client {client_id}")
        raise HTTPException(status_code=404, detail="Organization not found")

    db.delete(db_organization)
    db.commit()

    logger.info(f"Deleted organization {organization_id} for client {client_id}")
    return db_organization
