from typing import Optional
from pydantic import BaseModel

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str
    organization_id: int
    sla_condition_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None

    class Config:
        from_attributes = True

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None
    sla_condition_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None

    class Config:
        from_attributes = True

class ProjectSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: str
    organization_id: int
    sla_condition_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None

    class Config:
        from_attributes = True
