from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class EventSchema(BaseModel):
    name: str
    description: str
    start_date: str
    end_date: str
    organization_id: int
    class Config:
        from_attributes = True