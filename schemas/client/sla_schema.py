from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class SLASchema(BaseModel):
    name: str
    description: str


    class Config:
        from_attributes = True

class PrioritySchema(BaseModel):
    name: str
    description: str
    level: int


    class Config:
        from_attributes = True

class ImpactSchema(BaseModel):
    name: str
    description: str
    level: int


    class Config:
        from_attributes = True


class SLAConditionSchema(BaseModel):
    sla_policy_id: int
    priority_id: int
    impact_id: int
    response_time: int
    resolution_time: int

    class Config:
        orm_mode = True
