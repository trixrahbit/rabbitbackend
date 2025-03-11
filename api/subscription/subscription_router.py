from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from api.user.user_router import get_db
from models.models import Organization
from models.subscription.subscription_model import SubscriptionPlan as SQLASubscriptionPlan, Subscription as SQLASubscription
from root.root_elements import router
from schemas.subscription.subscription_schema import SubscriptionPlanCreate, SubscriptionCreate, SubscriptionPlan, Subscription


@router.get("/organizations/{client_id}/subscriptions", response_model=List[Subscription])
async def read_subscriptions(client_id: int, db: Session = Depends(get_db)):
    subscriptions = db.query(Organization).filter(Organization.clients_id == client_id).first().subscriptions
    return subscriptions


@router.post("/organizations/{client_id}/subscriptions", response_model=Subscription)
async def create_subscription(client_id: int, subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    subscription = SQLASubscription(**subscription.dict())
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription

@router.delete("/organizations/{client_id}/subscriptions/{subscription_id}", response_model=Subscription)
async def delete_subscription(client_id: int, subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(Organization).filter(Organization.clients_id == client_id).first().subscriptions.filter(SQLASubscription.id == subscription_id).first()
    db.delete(subscription)
    db.commit()
    return subscription
