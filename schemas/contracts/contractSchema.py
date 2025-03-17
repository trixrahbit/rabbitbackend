from typing import Optional
from pydantic import BaseModel

class ContractCreate(BaseModel):
    contract_number: str
    client_id: int
    start_date: str  # ISO date string, e.g. "2025-04-01"
    end_date: Optional[str] = None
    details: Optional[str] = None

    class Config:
        from_attributes = True

class ContractUpdate(BaseModel):
    contract_number: Optional[str] = None
    client_id: Optional[int] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    details: Optional[str] = None

    class Config:
        from_attributes = True

class ContractSchema(BaseModel):
    id: int
    contract_number: str
    client_id: int
    start_date: str
    end_date: Optional[str] = None
    details: Optional[str] = None

    class Config:
        from_attributes = True
