from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class AnnouncementSchema(BaseModel):
    title: str
    content: str
    organization_id: int


    class Config:
        from_attributes = True