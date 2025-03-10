from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class TimeEntryCreate(BaseModel):
    name: str
    user_id: int
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    ticket_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    date: Optional[datetime] = None
    hours: float
    description: Optional[str] = None

    class Config:
        from_attributes = True

class TimeEntryUpdate(BaseModel):
    name: Optional[str] = None
    user_id: Optional[int] = None
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    ticket_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    date: Optional[datetime] = None
    hours: Optional[float] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True

class TimeEntrySchema(BaseModel):
    id: int
    name: str
    user_id: int
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    ticket_id: Optional[int] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    date: Optional[datetime] = None
    hours: float
    description: Optional[str] = None

    class Config:
        from_attributes = True
