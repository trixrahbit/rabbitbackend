from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.models.models import Organization
from app.schemas.organizations.campagin_schema import CampaignSchema

router = APIRouter()


@router.get("/organizations/{client_id}/", response_model=List[CampaignSchema])
async def get_campaigns(client_id: int, db: Session = Depends(get_db)):
    campaigns = db.query(Organization).filter(Organization.client_id == client_id).all()
    return campaigns

@router.post("/organizations/{client_id}/", response_model=CampaignSchema)
async def create_campaign(client_id: int, campaign: CampaignSchema, db: Session = Depends(get_db)):
    new_campaign = Organization(**campaign.dict(), client_id=client_id)
    db.add(new_campaign)
    db.commit()
    db.refresh(new_campaign)
    return new_campaign

@router.patch("/organizations/{client_id}/{campaign_id}/", response_model=CampaignSchema)
async def update_campaign(client_id: int, campaign_id: int, campaign: CampaignSchema, db: Session = Depends(get_db)):
    db.query(Organization).filter(Organization.client_id == client_id).filter(Organization.campaign_id == campaign_id).update(campaign.dict())
    db.commit()
    updated_campaign = db.query(Organization).filter(Organization.client_id == client_id).filter(Organization.campaign_id == campaign_id).first()
    return updated_campaign

@router.delete("/organizations/{client_id}/{campaign_id}/", response_model=CampaignSchema)
async def delete_campaign(client_id: int, campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Organization).filter(Organization.client_id == client_id).filter(Organization.campaign_id == campaign_id).first()
    db.delete(campaign)
    db.commit()
    return campaign