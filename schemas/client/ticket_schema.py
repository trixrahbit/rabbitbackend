from typing import Optional
from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    subject: Optional[str] = None
    description: str
    status_id: int       # Changed from 'status'
    priority_id: int     # Changed from 'priority'
    impact_id: int       # Changed from 'impact'
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
    status_id: Optional[int] = None       # Changed from 'status'
    priority_id: Optional[int] = None     # Changed from 'priority'
    impact_id: Optional[int] = None       # Changed from 'impact'
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
    status_id: int         # Changed from 'status'
    priority_id: int       # Changed from 'priority'
    impact_id: int         # Changed from 'impact'
    created_at: Optional[str] = None
    resolved_at: Optional[str] = None
    sla_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None

    class Config:
        from_attributes = True
