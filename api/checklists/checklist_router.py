from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.user.user_router import get_db, router
from crudops.crud_checklist import create_checklist, update_checklist, get_checklist_by_task, get_checklists_by_story as crud_get_checklists_by_story
from schemas.checklist_schema import Checklist, ChecklistUpdate, ChecklistCreate



@router.post("/checklists/", response_model=Checklist)
def create_new_checklist(checklist: ChecklistCreate, db: Session = Depends(get_db)):
    print(checklist.dict())  # Log the incoming data for debugging
    return create_checklist(db, checklist)

@router.put("/checklists/{checklist_id}", response_model=Checklist)
def update_existing_checklist(checklist_id: int, checklist: ChecklistUpdate, db: Session = Depends(get_db)):
    db_checklist = update_checklist(db, checklist_id, checklist)
    if db_checklist is None:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return db_checklist

@router.get("/checklists/story/{story_id}", response_model=List[Checklist])
def get_checklists_by_story_handler(story_id: int, db: Session = Depends(get_db)):
    checklists = crud_get_checklists_by_story(db, story_id)
    return [Checklist.from_orm(checklist) for checklist in checklists]

@router.get("/checklists/task/{task_id}", response_model=List[Checklist])
def get_checklists_by_task_handler(task_id: int, db: Session = Depends(get_db)):
    checklists = get_checklist_by_task(db, task_id)
    return [Checklist.from_orm(checklist) for checklist in checklists]
