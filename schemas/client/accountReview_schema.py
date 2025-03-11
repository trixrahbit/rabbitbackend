from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class AccountReviewSchema(BaseModel):
    organization_id: int
    review_date: Optional[str] = None
    notes: Optional[str] = None
    follow_up_actions: Optional[str] = None
    creator_id: int
    updated_by_id: int

    class Config:
        from_attributes = True
