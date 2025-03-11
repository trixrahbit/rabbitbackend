from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class StrategicObjectiveSchema(BaseModel):
    organization_id: int
    objective: str
    target_completion_date: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True