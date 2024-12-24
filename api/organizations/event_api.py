from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.models import Organization
from models.organizationModels.event_model import Event
from schemas.organizations.event_schema import EventSchema

router = APIRouter()

@router.get("/{client_id}/events", response_model=List[EventSchema])
async def get_events(client_id: int, db: Session = Depends(get_db)):
    events = db.query(Organization).filter(Organization.client_id == client_id).first().events
    return events

@router.get("/{client_id}/events/{event_id}", response_model=EventSchema)
async def get_event(client_id: int, event_id: int, db: Session = Depends(get_db)):
    event = db.query(Organization).filter(Organization.client_id == client_id).first().events.filter(Event.id == event_id).first()
    return event

@router.post("/{client_id}/events", response_model=EventSchema)
async def create_event(client_id: int, event: EventSchema, db: Session = Depends(get_db)):
    event = Event(**event.dict())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

@router.patch("/{client_id}/events/{event_id}", response_model=EventSchema)
async def update_event(client_id: int, event_id: int, event: EventSchema, db: Session = Depends(get_db)):
    event = db.query(Organization).filter(Organization.client_id == client_id).first().events.filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    update_data = event.dict(exclude_unset=True)
    updated_event = db.query(Organization).filter(Organization.client_id == client_id).first().events.filter(Event.id == event_id).update(update_data)
    db.commit()
    return updated_event

@router.delete("/{client_id}/events/{event_id}", response_model=EventSchema)
async def delete_event(client_id: int, event_id: int, db: Session = Depends(get_db)):
    event = db.query(Organization).filter(Organization.client_id == client_id).first().events.filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    db.query(Organization).filter(Organization.client_id == client_id).first().events.filter(Event.id == event_id).delete()
    db.commit()
    return event
