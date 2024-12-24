from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class LocationSchema(BaseModel):
    organization_id: int
    name: str
    address: str
    phone: str

    class Config:
        from_attributes = True