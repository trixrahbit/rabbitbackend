import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.models import Client, Organization
from root.root_elements import router
from schemas.schemas import ClientSchema




# Existing endpoint for reading clients with pagination
@router.get("/organizations/{org_id}/clients/{client_id}", response_model=ClientSchema)
async def get_client_by_id(org_id: int, client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client



# New endpoint to return all clients in JSON format without pagination
@router.get("/organizations/{org_id}/clients", response_model=List[ClientSchema])
async def get_clients(org_id: int, db: Session = Depends(get_db)):
    clients = db.query(Client).filter(Client.organization_id == org_id).all()
    return clients


# Endpoint to get client ID based on client name
@router.get("/{org_id}/clients/{client_name}", response_model=ClientSchema)
async def get_client_id(org_id: int, client_name: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.client_name == client_name).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.post("/organizations/{org_id}/clients", response_model=ClientSchema)
async def create_client(org_id: int, client: ClientSchema, db: Session = Depends(get_db)):
    db_client = Client(**client.dict(), organization_id=org_id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@router.delete("/organizations/{org_id}/clients/{client_id}", response_model=ClientSchema)
async def delete_client(org_id: int, client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return client


@router.patch("/organizations/{org_id}/clients/{client_id}", response_model=ClientSchema)
async def update_client(org_id: int, client_id: int, client: ClientSchema, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    update_data = client.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client



#Endpoint to get client stats
@router.get("/{org_id}/clients/{client_id}/stats", response_model=ClientSchema)
async def get_client_stats(org_id: int, client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


