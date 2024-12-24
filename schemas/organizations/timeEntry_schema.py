from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr


class TimeEntrySchema(BaseModel):
    name: str
    description: str
    start_time: str
    end_time: str
    user_id: int
    project_id: Optional[int] = None
    task_id: Optional[int] = None
    ticket_id: Optional[int] = None
    date: str
    hours: float

    class Config:
        from_attributes = True