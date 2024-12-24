from fastapi import APIRouter, Depends, HTTPException
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.organizationModels.marketingAnalytics_model import MarketingAnalytics
from schemas.organizations.marketingAnalytics_schema import MarketingAnalyticsSchema

router = APIRouter()


@router.get("/{client_id}/marketingAnalytics", response_model=List[MarketingAnalyticsSchema])
async def get_all_marketing_analytics(client_id: int, db: Session = Depends(get_db)):
    marketing_analytics = db.query(MarketingAnalytics).filter(MarketingAnalytics.client_id == client_id).all()
    return marketing_analytics

@router.get("/{client_id}/marketingAnalytics/{marketing_analytics_id}", response_model=MarketingAnalyticsSchema)
async def get_marketing_analytics(client_id: int, marketing_analytics_id: int, db: Session = Depends(get_db)):
    marketing_analytics = db.query(MarketingAnalytics).filter(MarketingAnalytics.client_id == client_id).filter(MarketingAnalytics.id == marketing_analytics_id).first()
    if marketing_analytics is None:
        raise HTTPException(status_code=404, detail="Marketing Analytics not found")
    return marketing_analytics

@router.post("/{client_id}/marketingAnalytics", response_model=MarketingAnalyticsSchema)
async def create_marketing_analytics(client_id: int, marketing_analytics: MarketingAnalyticsSchema, db: Session = Depends(get_db)):
    marketing_analytics.client_id = client_id
    db.add(marketing_analytics)
    db.commit()
    db.refresh(marketing_analytics)
    return marketing_analytics

@router.patch("/{client_id}/marketingAnalytics/{marketing_analytics_id}", response_model=MarketingAnalyticsSchema)
async def update_marketing_analytics(client_id: int, marketing_analytics_id: int, marketing_analytics: MarketingAnalyticsSchema, db: Session = Depends(get_db)):
    db.query(MarketingAnalytics).filter(MarketingAnalytics.id == marketing_analytics_id).update(jsonable_encoder(marketing_analytics))
    db.commit()
    return marketing_analytics

@router.delete("/{client_id}/marketingAnalytics/{marketing_analytics_id}", response_model=MarketingAnalyticsSchema)
async def delete_marketing_analytics(client_id: int, marketing_analytics_id: int, db: Session = Depends(get_db)):
    marketing_analytics = db.query(MarketingAnalytics).filter(MarketingAnalytics.id == marketing_analytics_id).first()
    db.delete(marketing_analytics)
    db.commit()
    return marketing_analytics
