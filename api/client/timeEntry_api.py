from fastapi import Depends
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.clientModel.timeentry_model import TimeEntry
from root.root_elements import router
from schemas.organizations.timeEntry_schema import TimeEntrySchema


@router.get("/{client_id}/timeEntries", response_model=List[TimeEntrySchema])
async def get_timeEntries(client_id: int, db: Session = Depends(get_db)):
    timeEntries = db.query(TimeEntry).filter(TimeEntry.client_id == client_id).all()
    return timeEntries

@router.get("/{client_id}/timeEntries/{timeEntry_id}", response_model=TimeEntrySchema)
async def get_timeEntry(client_id: int, timeEntry_id: int, db: Session = Depends(get_db)):
    timeEntry = db.query(TimeEntry).filter(TimeEntry.id == timeEntry_id).first()
    return timeEntry

@router.get("/{client_id}/{org_id}/timeEntries", response_model=List[TimeEntrySchema])
async def get_timeEntries(client_id: int, org_id: int, db: Session = Depends(get_db)):
    timeEntries = db.query(TimeEntry).filter(TimeEntry.client_id == client_id).filter(TimeEntry.org_id == org_id).all()
    return timeEntries

@router.post("/{client_id}/timeEntries", response_model=TimeEntrySchema)
async def create_timeEntry(client_id: int, timeEntry: TimeEntrySchema, db: Session = Depends(get_db)):
    timeEntry = TimeEntry(**timeEntry.dict(), client_id=client_id)
    db.add(timeEntry)
    db.commit()
    db.refresh(timeEntry)
    return timeEntry

@router.patch("/{client_id}/timeEntries/{timeEntry_id}", response_model=TimeEntrySchema)
async def update_timeEntry(client_id: int, timeEntry_id: int, timeEntry: TimeEntrySchema, db: Session = Depends(get_db)):
    db.query(TimeEntry).filter(TimeEntry.id == timeEntry_id).update(jsonable_encoder(timeEntry))
    db.commit()
    return db.query(TimeEntry).filter(TimeEntry.id == timeEntry_id).first()

@router.delete("/{client_id}/timeEntries/{timeEntry_id}")
async def delete_timeEntry(client_id: int, timeEntry_id: int, db: Session = Depends(get_db)):
    db.query(TimeEntry).filter(TimeEntry.id == timeEntry_id).delete(synchronize_session=False)
    db.commit()
    return {"message": "TimeEntry deleted successfully!"}
