from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.models.organizationModels.services_model import Service
from app.schemas.organizations.services_schema import ServiceSchema

router = APIRouter()

@router.get("/{client_id}/services", response_model=List[ServiceSchema])
async def get_services(client_id: int, db: Session = Depends(get_db)):
    services = db.query(Service).filter(Service.client_id == client_id).all()
    return services

@router.get("/{client_id}/services/{service_id}", response_model=ServiceSchema)
async def get_service(client_id: int, service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.client_id == client_id, Service.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return service

@router.post("/{client_id}/services", response_model=ServiceSchema)
async def create_service(client_id: int, service: ServiceSchema, db: Session = Depends(get_db)):
    db_service = Service(client_id=client_id, **service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.patch("/{client_id}/services/{service_id}", response_model=ServiceSchema)
async def update_service(client_id: int, service_id: int, service: ServiceSchema, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.client_id == client_id, Service.id == service_id).first()
    if db_service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    update_data = service.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_service, key, value)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/{client_id}/services/{service_id}", response_model=ServiceSchema)
async def delete_service(client_id: int, service_id: int, db: Session = Depends(get_db)):
    service = db.query(Service).filter(Service.client_id == client_id, Service.id == service_id).first()
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(service)
    db.commit()
    return service
