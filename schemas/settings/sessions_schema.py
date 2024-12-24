from pydantic import BaseModel, constr, EmailStr


class SessionCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=7)
    remember_me: bool = False
    class Config:
        from_attributes = True

class Session(BaseModel):
    email: EmailStr
    token: str
    start_date: str
    end_date: str
    status: str
    location: str
    class Config:
        from_attributes = True

class SessionUpdate(BaseModel):
    token: str
    end_date: str
    status: str
    location: str
    class Config:
        from_attributes = True

class SessionDelete(BaseModel):
    token: str
    class Config:
        from_attributes = True