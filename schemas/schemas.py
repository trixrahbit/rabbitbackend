from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr, validator


class ClientSchema(BaseModel):
    id: int
    name: str
    domain: str
    phone: Optional[str] = None
    creator_id: Optional[int] = None
    organization_id: int
    type: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    revenue: Optional[str] = None
    founded: Optional[str] = None

    class Config:
        from_attributes = True


class ClientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str
    creator_id: int
    organization_id: int


class OrganizationSchema(BaseModel):
    name: str
    domain: str
    phone: Optional[str] = None
    creator_id: Optional[int] = None
    type: Optional[str] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    description: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    revenue: Optional[str] = None
    founded: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
    password: constr(min_length=7)
    agree_to_terms: bool
    organization_id: int
    creator_id: Optional[int] = None
    type: Optional[str] = None
    organization_id: int

    # Use Config to define model behavior with SQLAlchemy if needed
    class Config:
        from_attributes = True


class RoleSchema(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class RoleCreateSchema(BaseModel):
    name: str
    is_default: bool = False


class UserList(BaseModel):
    id: int
    name: str
    email: str
    username: str
    mobile: Optional[str] = None
    location: Optional[str] = None
    roles: Optional[List[RoleSchema]] = []

    class Config:
        from_attributes = True


class BusinessHoursSchema(BaseModel):
    day_of_week: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None

    @validator('start_time', 'end_time', pre=True, always=True)
    def empty_str_to_none(cls, v):
        return v or None

class UserUpdateSchema(BaseModel):
    name: Optional[str]
    email: Optional[str]
    booking_url: Optional[str]
    business_hours: Optional[List[BusinessHoursSchema]]
    time_zone: Optional[str]
    outlook_token_expires_at: Optional[str]

class TimeZoneUpdate(BaseModel):
    time_zone: str

