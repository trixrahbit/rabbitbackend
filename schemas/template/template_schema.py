from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class TemplateBase(BaseModel):
    name: str
    description: Optional[str]
    methodology: str

class TemplateCreate(TemplateBase):
    phases: List['PhaseCreate'] = []
    tasks: List['TaskCreate'] = []
    sprints: List['SprintCreate'] = []
    stories: List['StoryCreate'] = []

class Template(TemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime
    phases: List['Phase'] = []
    tasks: List['Task'] = []
    sprints: List['Sprint'] = []
    stories: List['Story'] = []

    class Config:
        from_attributes = True

class PhaseBase(BaseModel):
    name: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    budget_hours: Optional[float]
    template_id: int

class PhaseCreate(PhaseBase):
    id: Optional[int]  # Allow id to be optional for update purposes
    tasks: List['TaskCreate'] = []

class Phase(PhaseBase):
    id: int
    tasks: List['Task'] = []

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    name: str
    description: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    budget_hours: Optional[float]
    phase_id: Optional[int]
    template_id: int

class TaskCreate(TaskBase):
    id: Optional[int]  # Allow id to be optional for update purposes

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True

class SprintBase(BaseModel):
    name: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    budget_hours: Optional[float]
    template_id: int

class SprintCreate(SprintBase):
    id: Optional[int]  # Allow id to be optional for update purposes
    stories: List['StoryCreate'] = []

class Sprint(SprintBase):
    id: int
    stories: List['Story'] = []

    class Config:
        from_attributes = True

class StoryBase(BaseModel):
    name: str
    description: Optional[str]
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    budget_hours: Optional[float]
    sprint_id: Optional[int]
    template_id: int

class StoryCreate(StoryBase):
    id: Optional[int]  # Allow id to be optional for update purposes

class Story(StoryBase):
    id: int

    class Config:
        from_attributes = True
