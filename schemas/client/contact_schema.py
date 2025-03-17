from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class ContactSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    client_id: int

    class Config:
        from_attributes = True

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    client_id: int

    class Config:
        from_attributes = True

class ContactUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    role: Optional[str]
    client_id: int

    class Config:
        from_attributes = True