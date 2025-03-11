from fastapi import Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.organizationModels.subscription_model import Subscription
from root.root_elements import router
from schemas.client.subscription_schema import SubscriptionSchema



@router.get("{client_id}/subscriptions", response_model=List[SubscriptionSchema])
def get_subscriptions(client_id: int, db: Session = Depends(get_db)):
    subscriptions = db.query(Subscription).filter(Subscription.client_id == client_id).all()
    return subscriptions

@router.get("{client_id}/subscriptions/{subscription_id}", response_model=SubscriptionSchema)
def get_subscription(client_id: int, subscription_id: int, db: Session = Depends(get_db)):
    subscription = db.query(Subscription).filter(Subscription.client_id == client_id, Subscription.id == subscription_id).first()
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@router.post("{client_id}/subscriptions", response_model=SubscriptionSchema)
def create_subscription(client_id: int, subscription: SubscriptionSchema, db: Session = Depends(get_db)):
    db_subscription = Subscription(client_id=client_id, **subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.patch("{client_id}/subscriptions/{subscription_id}", response_model=SubscriptionSchema)
def update_subscription(client_id: int, subscription_id: int, subscription: SubscriptionSchema, db: Session = Depends(get_db)):
    db_subscription = db.query(Subscription).filter(Subscription.client_id == client_id, Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    update_data = subscription.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subscription, key, value)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

@router.delete("{client_id}/subscriptions/{subscription_id}", response_model=SubscriptionSchema)
def delete_subscription(client_id: int, subscription_id: int, db: Session = Depends(get_db)):
    db_subscription = db.query(Subscription).filter(Subscription.client_id == client_id, Subscription.id == subscription_id).first()
    if db_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    db.delete(db_subscription)
    db.commit()
    return db_subscription