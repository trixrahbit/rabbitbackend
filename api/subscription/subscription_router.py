from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from db_config.db_connection import get_db
from models.models import Organization
from models.subscription.subscription_model import SubscriptionPlan as SQLASubscriptionPlan, Subscription as SQLASubscription
from root.root_elements import router
from schemas.subscription.subscription_schema import SubscriptionPlanCreate, SubscriptionCreate, SubscriptionPlan, Subscription


@router.get("/organizations/{org_id}/subscriptions", response_model=List[Subscription])
async def read_subscriptions(org_id: int, db: Session = Depends(get_db)):
    subscriptions = db.query(Organization).filter(Organization.id == org_id).first().subscriptions
    return subscriptions

@router.post("/organizations/{org_id}/subscriptions", response_model=Subscription)
async def create_subscription(org_id: int, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    subscription = SQLASubscription(**subscription.dict())
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

@router.patch("/organizations/{org_id}/subscriptions/{subscription_id}", response_model=Subscription)
async def update_subscription(org_id: int, subscription_id: int, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = db.query(Organization).filter(Organization.id == org_id).first().subscriptions.filter(SQLASubscription.id == subscription_id).first()
    update_data = subscription.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subscription, key, value)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

