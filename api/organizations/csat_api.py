from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.models.models import Organization
from app.schemas.organizations.accountReview_schema import AccountReviewSchema

router = APIRouter()


@router.get("/organizations/{client_id}/{org_id}/csat", response_model=List[AccountReviewSchema])
async def read_csat(client_id: int, org_id: int, db: Session = Depends(get_db)):
    """
    Retrieve CSAT for an organization
    """
    csat = db.query(Organization).filter(Organization.id == org_id).first()
    if not csat:
        raise HTTPException(status_code=404, detail="CSAT not found")
    return csat