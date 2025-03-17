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
    domain: Optional[str] = None
    logo: Optional[str] = None
    website: Optional[str] = None
    revenue: Optional[str] = None
    founded: Optional[str] = None

    class Config:
        from_attributes = True  # ✅ Ensures correct ORM conversion


class ClientCreate(BaseModel):
    name: str
    domain: str
    phone: str
    creator_id: int
    organization_id: int

    class Config:
        from_attributes = True

class OrganizationSchema(BaseModel):
    id: int
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
    company_name: constr(min_length=1)

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
    session_timeout: Optional[int] = 30  # ✅ Include session timeout in API responses

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
    session_timeout: Optional[int]  # ✅ Allow updating session timeout

class TimeZoneUpdate(BaseModel):
    time_zone: str

class SessionTimeoutUpdateSchema(BaseModel):
    session_timeout: int
