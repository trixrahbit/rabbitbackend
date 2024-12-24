from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CalendarEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None

class CalendarEventCreate(CalendarEventBase):
    user_id: int
    client_id: int  # Add client_id to the create schema

class CalendarEventUpdate(CalendarEventBase):
    pass

class CalendarEvent(CalendarEventBase):
    id: int
    user_id: int
    client_id: int  # Include client_id in the response schema
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserBookingUrlUpdate(BaseModel):
    booking_url: str

    class Config:
        from_attributes = True  # Ensure compatibility with Pydantic's ORM mode