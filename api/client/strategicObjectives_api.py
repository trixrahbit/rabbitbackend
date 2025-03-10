from fastapi import Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.clientModel.strategicObjectives_model import StrategicObjective
from root.root_elements import router
from schemas.organizations.strategicObjectives_schema import StrategicObjectiveSchema



@router.get("{client_id}/strategicObjectives", response_model=List[StrategicObjectiveSchema])
async def read_strategicObjectives(client_id: int, db: Session = Depends(get_db)):
    strategicObjectives = db.query(StrategicObjective).filter(StrategicObjective.client_id == client_id).all()
    return strategicObjectives

@router.get("{client_id}/strategicObjectives/{strategicObjective_id}", response_model=StrategicObjectiveSchema)
async def read_strategicObjective(client_id: int, strategicObjective_id: int, db: Session = Depends(get_db)):
    strategicObjective = db.query(StrategicObjective).filter(StrategicObjective.client_id == client_id, StrategicObjective.id == strategicObjective_id).first()
    if not strategicObjective:
        raise HTTPException(status_code=404, detail="Strategic Objective not found")
    return strategicObjective

@router.post("{client_id}/strategicObjectives", response_model=StrategicObjectiveSchema)
async def create_strategicObjective(client_id: int, strategicObjective: StrategicObjectiveSchema, db: Session = Depends(get_db)):
    db_strategicObjective = StrategicObjective(client_id=client_id, **strategicObjective.dict())
    db.add(db_strategicObjective)
    db.commit()
    db.refresh(db_strategicObjective)
    return db_strategicObjective

@router.patch("{client_id}/strategicObjectives/{strategicObjective_id}", response_model=StrategicObjectiveSchema)
async def update_strategicObjective(client_id: int, strategicObjective_id: int, strategicObjective: StrategicObjectiveSchema, db: Session = Depends(get_db)):
    db_strategicObjective = db.query(StrategicObjective).filter(StrategicObjective.client_id == client_id, StrategicObjective.id == strategicObjective_id).first()
    if not db_strategicObjective:
        raise HTTPException(status_code=404, detail="Strategic Objective not found")
    update_data = strategicObjective.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_strategicObjective, key, value)
    db.commit()
    db.refresh(db_strategicObjective)
    return db_strategicObjective

@router.delete("{client_id}/strategicObjectives/{strategicObjective_id}", response_model=StrategicObjectiveSchema)
async def delete_strategicObjective(client_id: int, strategicObjective_id: int, db: Session = Depends(get_db)):
    db_strategicObjective = db.query(StrategicObjective).filter(StrategicObjective.client_id == client_id, StrategicObjective.id == strategicObjective_id).first()
    if not db_strategicObjective:
        raise HTTPException(status_code=404, detail="Strategic Objective not found")
    db.delete(db_strategicObjective)
    db.commit()
    return db_strategicObjective