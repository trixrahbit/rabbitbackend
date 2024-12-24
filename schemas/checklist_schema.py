from pydantic import BaseModel, model_validator
from typing import List, Optional
from datetime import datetime

class ChecklistItemBase(BaseModel):
    description: str
    completed: bool = False
    completed_by: Optional[str] = None
    completed_at: Optional[datetime] = None
    order: int = 0  # New field for item order

class ChecklistItemCreate(ChecklistItemBase):
    pass

class ChecklistItemUpdate(ChecklistItemBase):
    pass

class ChecklistItem(ChecklistItemBase):
    id: int
    checklist_id: int

    class Config:
        orm_mode = True
        from_attributes = True  # Enable from_orm functionality

class ChecklistBase(BaseModel):
    name: str  # New field for checklist name

class ChecklistCreate(ChecklistBase):
    task_id: Optional[int] = None
    story_id: Optional[int] = None
    items: List[ChecklistItemCreate] = []

    @model_validator(mode='before')
    def check_either_task_or_story(cls, values):
        task_id, story_id = values.get('task_id'), values.get('story_id')
        if not task_id and not story_id:
            raise ValueError('Either task_id or story_id must be provided')
        if task_id and story_id:
            raise ValueError('Only one of task_id or story_id should be provided')
        return values

class ChecklistUpdate(ChecklistBase):
    items: List[ChecklistItemUpdate] = []

class Checklist(ChecklistBase):
    id: int
    task_id: Optional[int]
    story_id: Optional[int]
    created_at: datetime
    updated_at: datetime
    items: List[ChecklistItem] = []

    class Config:
        orm_mode = True
        from_attributes = True  # Enable from_orm functionality
