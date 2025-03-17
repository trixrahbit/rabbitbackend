from typing import Optional
from pydantic import BaseModel

class TicketCreate(BaseModel):
    title: str
    subject: Optional[str] = None
    description: str
    status_id: int          # changed from "status"
    priority_id: int        # changed from "priority"
    impact_id: int          # changed from "impact"
    sla_condition_id: Optional[int] = None  # changed from "sla_id"
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None

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
    sla_condition_id: Optional[int] = None  # changed from "sla_id"
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
    status_id: int
    priority_id: int
    impact_id: int
    created_at: Optional[str] = None
    resolved_at: Optional[str] = None
    sla_condition_id: Optional[int] = None  # changed from "sla_id"
    organization_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    contact_id: Optional[int] = None

    class Config:
        from_attributes = True
