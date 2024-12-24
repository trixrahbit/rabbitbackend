from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class StoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget_hours: Optional[float] = None
    sprint_id: Optional[int] = None
    project_id: Optional[int] = None


class StoryCreate(StoryBase):
    pass


class Story(StoryBase):
    id: int

    class Config:
        orm_mode: True


class SprintBase(BaseModel):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget_hours: Optional[float] = None
    project_id: Optional[int] = None


class SprintCreate(SprintBase):
    stories: List[StoryCreate] = []


class Sprint(SprintBase):
    id: int
    stories: List[Story] = []

    class Config:
        orm_mode: True


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget_hours: Optional[float] = None
    phase_id: Optional[int] = None
    project_id: Optional[int] = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int

    class Config:
        orm_mode: True


class PhaseBase(BaseModel):
    name: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget_hours: Optional[float] = None
    project_id: Optional[int] = None


class PhaseCreate(PhaseBase):
    tasks: List[TaskCreate] = []


class Phase(PhaseBase):
    id: int
    tasks: List[Task] = []

    class Config:
        orm_mode: True


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None
    client_id: int
    methodology: str


class ProjectCreate(ProjectBase):
    phases: List[PhaseCreate] = []
    tasks: List[TaskCreate] = []
    sprints: List[SprintCreate] = []
    stories: List[StoryCreate] = []


class Project(ProjectBase):
    id: int
    phases: List[Phase] = []
    tasks: List[Task] = []
    sprints: List[Sprint] = []
    stories: List[Story] = []

    class Config:
        orm_mode: True


# New Template Classes
class TemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    methodology: str


class TemplateCreate(TemplateBase):
    pass


class Template(TemplateBase):
    id: int

    class Config:
        orm_mode: True


class StoryUpdate(StoryBase):
    pass

class SprintUpdate(SprintBase):
    pass

class TaskUpdate(TaskBase):
    pass

class PhaseUpdate(PhaseBase):
    pass
