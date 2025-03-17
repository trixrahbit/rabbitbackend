from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db_config.db_connection import get_db
from models.ticket.queueModel import Queue
from models.ticket.ticketinfo_Models import Priority, Impact, Status
from root.root_elements import router
from schemas.client.ticket_schema import QueueSchema
from schemas.ticket.ticketinfo_Schema import PrioritySchema, PriorityCreate, ImpactSchema, ImpactCreate, StatusSchema, StatusCreate


# 🔹 Get all priorities
@router.get("/priorities", response_model=List[PrioritySchema])
async def get_priorities(db: Session = Depends(get_db)):
    return db.query(Priority).all()

# 🔹 Get priority by ID
@router.get("/priorities/{priority_id}", response_model=PrioritySchema)
async def get_priority(priority_id: int, db: Session = Depends(get_db)):
    priority = db.query(Priority).filter(Priority.id == priority_id).first()
    if not priority:
        raise HTTPException(status_code=404, detail="Priority not found")
    return priority

# 🔹 Create new priority
@router.post("/priorities", response_model=PrioritySchema)
async def create_priority(priority: PriorityCreate, db: Session = Depends(get_db)):
    new_priority = Priority(name=priority.name, description=priority.description)
    db.add(new_priority)
    db.commit()
    db.refresh(new_priority)
    return new_priority

# 🔹 Get all impacts
@router.get("/impacts", response_model=List[ImpactSchema])
async def get_impacts(db: Session = Depends(get_db)):
    return db.query(Impact).all()

# 🔹 Get impact by ID
@router.get("/impacts/{impact_id}", response_model=ImpactSchema)
async def get_impact(impact_id: int, db: Session = Depends(get_db)):
    impact = db.query(Impact).filter(Impact.id == impact_id).first()
    if not impact:
        raise HTTPException(status_code=404, detail="Impact not found")
    return impact

# 🔹 Create new impact
@router.post("/impacts", response_model=ImpactSchema)
async def create_impact(impact: ImpactCreate, db: Session = Depends(get_db)):
    new_impact = Impact(name=impact.name, description=impact.description)
    db.add(new_impact)
    db.commit()
    db.refresh(new_impact)
    return new_impact

# 🔹 Get all statuses
@router.get("/statuses", response_model=List[StatusSchema])
async def get_statuses(db: Session = Depends(get_db)):
    return db.query(Status).all()

# 🔹 Get status by ID
@router.get("/statuses/{status_id}", response_model=StatusSchema)
async def get_status(status_id: int, db: Session = Depends(get_db)):
    status = db.query(Status).filter(Status.id == status_id).first()
    if not status:
        raise HTTPException(status_code=404, detail="Status not found")
    return status

# 🔹 Create new status
@router.post("/statuses", response_model=StatusSchema)
async def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    new_status = Status(name=status.name, description=status.description)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status


@router.get("/queues", response_model=List[QueueSchema])
async def get_queues(db: Session = Depends(get_db)):
    return db.query(Queue).all()
