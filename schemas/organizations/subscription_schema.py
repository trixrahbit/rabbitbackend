from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class SubscriptionSchema(BaseModel):
    name: str
    domain: str
    phone: Optional[str] = None
    creator_id: Optional[int] = None
    class Config:
        from_attributes = True