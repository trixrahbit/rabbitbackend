from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

from app.schemas.schemas import RoleSchema


class ProfileList(BaseModel):
    id: int
    name: str
    email: str
    username: str
    email: str
    mobile: str
    location: str
    roles: Optional[List[RoleSchema]] = []

    class Config:
        from_attributes = True