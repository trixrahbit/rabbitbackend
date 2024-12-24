from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class SubscriptionPlanBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    features: Optional[dict]

class SubscriptionPlanCreate(SubscriptionPlanBase):
    pass

class SubscriptionPlan(SubscriptionPlanBase):
    id: int
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class SubscriptionBase(BaseModel):
    client_id: int
    plan_id: int
    start_date: date
    end_date: Optional[date]
    is_active: Optional[bool] = True

class SubscriptionCreate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    created_at: date
    updated_at: date
    plan: SubscriptionPlan

    class Config:
        orm_mode = True
