from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class IncidentSchema(BaseModel):
    title: str
    description: str
    priority: str
    status: str
    opened_at: Optional[str] = None
    closed_at: Optional[str] = None
    organization_id: int
    
    class Config:
        from_attributes = True