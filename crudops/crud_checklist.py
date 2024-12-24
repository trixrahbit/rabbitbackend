from sqlalchemy.orm import Session
from models.checklist_model import Checklist as DBChecklist, ChecklistItem as DBChecklistItem, Checklist, \
    ChecklistItem
from schemas.checklist_schema import ChecklistCreate, ChecklistUpdate, Checklist as ChecklistSchema


def create_checklist(db: Session, checklist: ChecklistCreate):
    # Validate that only one ID is provided
    if checklist.task_id and checklist.story_id:
        raise ValueError("Only one of task_id or story_id should be provided, not both.")

    if checklist.task_id:
        task_id = checklist.task_id
        story_id = None
    elif checklist.story_id:
        task_id = None
        story_id = checklist.story_id
    else:
        raise ValueError("Either task_id or story_id must be provided.")

    # Create the checklist instance
    db_checklist = DBChecklist(
        task_id=task_id,
        story_id=story_id,
        items=[DBChecklistItem(**item.dict()) for item in checklist.items],
    )

    db.add(db_checklist)
    db.commit()
    db.refresh(db_checklist)

    return db_checklist


def get_checklists_by_story(db: Session, story_id: int):
    checklists = db.query(Checklist).filter(Checklist.story_id == story_id).all()
    return [ChecklistSchema.from_orm(checklist) for checklist in checklists]

def get_checklist_by_task(db: Session, task_id: int):
    return db.query(DBChecklist).filter(DBChecklist.task_id == task_id).all()

def update_checklist(db: Session, checklist_id: int, checklist: ChecklistUpdate):
    db_checklist = db.query(DBChecklist).filter(DBChecklist.id == checklist_id).first()
    if not db_checklist:
        return None

    for item_data in checklist.items:
        item = db.query(ChecklistItem).filter(ChecklistItem.id == item_data.id).first()
        if item:
            for key, value in item_data.dict().items():
                setattr(item, key, value)
        else:
            new_item = ChecklistItem(**item_data.dict(), checklist_id=checklist_id)
            db.add(new_item)

    db.commit()
    db.refresh(db_checklist)
    return db_checklist

def delete_checklist(db: Session, checklist_id: int):
    db_checklist = db.query(DBChecklist).filter(DBChecklist.id == checklist_id).first()
    db.delete(db_checklist)
    db.commit()
