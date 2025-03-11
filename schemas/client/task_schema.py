from typing import Optional
from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[str] = None
    project_id: int
    sla_condition_id: Optional[int] = None

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[str] = None
    sla_condition_id: Optional[int] = None

    class Config:
        from_attributes = True

class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: str
    priority: str
    due_date: Optional[str] = None
    project_id: int
    sla_condition_id: Optional[int] = None

    class Config:
        from_attributes = True
