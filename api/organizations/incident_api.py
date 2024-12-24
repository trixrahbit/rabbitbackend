from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.models.models import Organization
from app.models.organizationModels.incident_model import IncidentReport
from app.schemas.organizations.incident_schema import IncidentSchema

router = APIRouter()


@router.get("/organizations/{client_id}/incidents", response_model=List[IncidentSchema])
async def read_incidents(client_id: int, db: Session = Depends(get_db)):
    incidents = db.query(Organization).filter(Organization.client_id == client_id).first().incidents
    return incidents

@router.get("/organizations/{client_id}/incidents/{incident_id}", response_model=IncidentSchema)
async def read_incident(client_id: int, incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Organization).filter(Organization.client_id == client_id).first().incidents.filter(IncidentReport.id == incident_id).first()
    return incident

@router.get("/organizations/{client_id}/{org_id}incidents/{incident_id}/", response_model=IncidentSchema)
async def read_incident(client_id: int, org_id: int, incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Organization).filter(Organization.client_id == client_id).first().incidents.filter(IncidentReport.id == incident_id).first()
    return incident

@router.post("/organizations/{client_id}/incidents", response_model=IncidentSchema)
async def create_incident(client_id: int, incident: IncidentSchema, db: Session = Depends(get_db)):
    incident = IncidentReport(**incident.dict())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@router.patch("/organizations/{client_id}/incidents/{incident_id}", response_model=IncidentSchema)
async def update_incident(client_id: int, incident_id: int, incident: IncidentSchema, db: Session = Depends(get_db)):
    db_incident = db.query(Organization).filter(Organization.client_id == client_id).first().incidents.filter(IncidentReport.id == incident_id).first()
    update_data = incident.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_incident, key, value)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.delete("/organizations/{client_id}/incidents/{incident_id}", response_model=IncidentSchema)
async def delete_incident(client_id: int, incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(Organization).filter(Organization.client_id == client_id).first().incidents.filter(IncidentReport.id == incident_id).first()
    db.delete(incident)
    db.commit()
    return incident