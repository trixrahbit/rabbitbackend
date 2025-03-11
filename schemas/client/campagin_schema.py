from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class CampaignSchema(BaseModel):
    name: str
    type: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    budget: Optional[float] = None
    spent: Optional[float] = None
    leads_generated: Optional[int] = None
    deals_closed: Optional[int] = None
    roi: Optional[float] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True