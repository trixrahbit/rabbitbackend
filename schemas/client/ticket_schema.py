# schemas/client/ticket_schema.py
from typing import Optional
from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    subject: Optional[str] = None
    description: str
    status_id: int
    priority_id: int
    impact_id: int
    sla_condition_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None
    queue_id: Optional[int] = None    # NEW

    class Config:
        from_attributes = True

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    status_id: Optional[int] = None
    priority_id: Optional[int] = None
    impact_id: Optional[int] = None
    resolved_at: Optional[str] = None
    sla_condition_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None
    queue_id: Optional[int] = None    # NEW

    class Config:
        from_attributes = True

class TicketSchema(BaseModel):
    id: int
    title: str
    subject: Optional[str] = None
    description: str
    status_id: int
    priority_id: int
    impact_id: int
    created_at: Optional[str] = None
    resolved_at: Optional[str] = None
    sla_condition_id: Optional[int] = None
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None
    queue_id: Optional[int] = None    # NEW

    class Config:
        from_attributes = True
