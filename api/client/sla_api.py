from fastapi import Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from db_config.db_connection import get_db
from models.clientModel.sla_model import SLA
from root.root_elements import router
from schemas.client.sla_schema import SLASchema


@router.get("/sla", response_model=List[SLASchema])
async def get_sla(db: Session = Depends(get_db)):
    sla = db.query(SLA).all()
    return sla

@router.get("/{client_id}/sla", response_model=List[SLASchema])
async def get_sla(client_id: int, db: Session = Depends(get_db)):
    sla = db.query(SLA).filter(SLA.client_id == client_id).all()
    return sla

@router.get("/{client_id}/sla/{sla_id}", response_model=SLASchema)
async def get_sla(client_id: int, sla_id: int, db: Session = Depends(get_db)):
    sla = db.query(SLA).filter(SLA.client_id == client_id, SLA.id == sla_id).first()
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    return sla


@router.post("/{client_id}/sla", response_model=SLASchema)
async def create_sla(client_id: int, sla: SLASchema, db: Session = Depends(get_db)):
    db_sla = SLA(client_id=client_id, **sla.dict())
    db.add(db_sla)
    db.commit()
    db.refresh(db_sla)
    return db_sla

@router.patch("/{client_id}/sla/{sla_id}", response_model=SLASchema)
async def update_sla(client_id: int, sla_id: int, sla: SLASchema, db: Session = Depends(get_db)):
    db_sla = db.query(SLA).filter(SLA.client_id == client_id, SLA.id == sla_id).first()
    if not db_sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    update_data = sla.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_sla, key, value)
    db.commit()
    db.refresh(db_sla)
    return db_sla

@router.delete("/{client_id}/sla/{sla_id}", response_model=SLASchema)
async def delete_sla(client_id: int, sla_id: int, db: Session = Depends(get_db)):
    sla = db.query(SLA).filter(SLA.client_id == client_id, SLA.id == sla_id).first()
    if not sla:
        raise HTTPException(status_code=404, detail="SLA not found")
    db.delete(sla)
    db.commit()
    return sla