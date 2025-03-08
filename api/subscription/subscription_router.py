from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from api.user.user_router import get_db
from models.subscription.subscription_model import SubscriptionPlan as SQLASubscriptionPlan, Subscription as SQLASubscription
from root.root_elements import router
from schemas.subscription.subscription_schema import SubscriptionPlanCreate, SubscriptionCreate, SubscriptionPlan, Subscription


@router.post("/subscription-plans/", response_model=SubscriptionPlan)
def create_subscription_plan(plan: SubscriptionPlanCreate, db: Session = Depends(get_db)):
    db_plan = SQLASubscriptionPlan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan  # FastAPI will convert this SQLAlchemy model to a Pydantic model

@router.post("/subscriptions/", response_model=Subscription)
def create_subscription(subscription: SubscriptionCreate, db: Session = Depends(get_db)):
    db_subscription = SQLASubscription(**subscription.dict())
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription  # FastAPI will convert this SQLAlchemy model to a Pydantic model

@router.get("/clients/{client_id}/subscriptions", response_model=List[Subscription])
def get_client_subscriptions(client_id: int, db: Session = Depends(get_db)):
    subscriptions = db.query(SQLASubscription).filter(SQLASubscription.client_id == client_id).all()
    return subscriptions  # FastAPI will convert this list of SQLAlchemy models to a list of Pydantic models
