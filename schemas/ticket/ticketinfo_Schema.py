from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PrioritySchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PriorityCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ImpactSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ImpactCreate(BaseModel):
    name: str
    description: Optional[str] = None

class StatusSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class StatusCreate(BaseModel):
    name: str
    description: Optional[str] = None
