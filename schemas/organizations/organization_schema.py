from pydantic import BaseModel
from typing import Optional



class OrganizationTypeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class IndustrySchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class OrganizationSizeSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True