from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class TaskSchema(BaseModel):
    title: str
    description: str
    status: str
    priority: str
    due_date: Optional[str] = None
    project_id: int
    
    class Config:
        from_attributes = True
