from typing import Optional
from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    subject: Optional[str] = None
    description: str
    status: str
    priority: str
    impact: str
    sla_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None

    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    impact: Optional[str] = None
    resolved_at: Optional[str] = None
    sla_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None

    class Config:
        from_attributes = True

class TicketSchema(BaseModel):
    id: int
    title: str
    subject: Optional[str] = None
    description: str
    status: str
    priority: str
    impact: str
    created_at: Optional[str] = None
    resolved_at: Optional[str] = None
    sla_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None

    class Config:
        from_attributes = True
