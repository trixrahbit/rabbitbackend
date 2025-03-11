from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class AssetSchema(BaseModel):
    name: str
    type: str
    description: Optional[str] = None
    organization_id: int
    status: Optional[str] = None
    project_id: Optional[int] = None
    billing_agreement_id: Optional[int] = None
    creator_id: int
    last_updated_by_id: int


    class Config:
        from_attributes = True

class AssetTypeSchema(BaseModel):
    name: str
    description: Optional[str] = None
    creator_id: int
    last_updated_by_id: int

    class Config:
        from_attributes = True