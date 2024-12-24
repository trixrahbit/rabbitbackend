from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class ProjectSchema(BaseModel):
    name: str
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    status: Optional[str] = None
    organization_id: Optional[int] = None
    
    class Config:
        from_attributes = True