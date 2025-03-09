from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class TicketSchema(BaseModel):
    id: int
    title: str
    subject: str
    description: str
    status: str
    priority: str
    impact: str
    created_at: Optional[str] = None
    resolved_at: Optional[str] = None
    sla_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    
    class Config:
        from_attributes = True