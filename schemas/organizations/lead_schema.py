from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class LeadSchema(BaseModel):
    name: str
    email: str
    phone: str
    source: str
    status: str
    campaign_id: int
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    organization_id: int
    class Config:
        from_attributes = True