from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class CSATSchema(BaseModel):
    title: str
    description: Optional[str] = None
    sent_date: Optional[str] = None
    response_rate: Optional[str] = None
    class Config:
        from_attributes = True