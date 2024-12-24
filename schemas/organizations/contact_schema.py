from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class ContactSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    role: str
    organization_id: int