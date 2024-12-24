from typing import Optional

from pydantic import BaseModel
from datetime import datetime

class BookingLinkBase(BaseModel):
    name: str

class BookingLinkCreate(BaseModel):
    name: str
    duration: int  # Duration in minutes

class BookingLink(BookingLinkBase):
    id: int
    url: str
    duration: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class EventRequest(BaseModel):
    meeting_uuid: str  # Change from meeting_url to meeting_uuid
    visitor_name: str
    visitor_email: str
    cc_emails: Optional[str]
    notes: Optional[str]
    start_datetime: datetime
    end_datetime: datetime
