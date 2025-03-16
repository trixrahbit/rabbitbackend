from fastapi import Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from db_config.db_connection import get_db
from models.models import Organization
from root.root_elements import router
from schemas.client.accountReview_schema import AccountReviewSchema



@router.get("/organizations/{client_id}/{org_id}/csat", response_model=List[AccountReviewSchema])
async def read_csat(client_id: int, org_id: int, db: Session = Depends(get_db)):
    """
    Retrieve CSAT for an organization
    """
    csat = db.query(Organization).filter(Organization.id == org_id).first()
    if not csat:
        raise HTTPException(status_code=404, detail="CSAT not found")
    return csat