from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class ServiceSchema(BaseModel):
    name: str
    description: str
    monthly_cost: float
    
    class Config:
        from_attributes = True