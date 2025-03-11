from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class DealSchema(BaseModel):
    name: str
    organization_id: int
    value: float
    stage: str
    expected_close_date: str
    actual_close_date: Optional[str] = None

    class Config:
        from_attributes = True