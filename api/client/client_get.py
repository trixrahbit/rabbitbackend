from loguru import logger
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from db_config.db_connection import get_db
from models.models import Client, Organization
from root.root_elements import router
from schemas.schemas import ClientSchema, ClientCreate  # Ensure schema exists


# 🔹 Get a client by ID under a specific organization
@router.get("/organizations/{org_id}/clients/{client_id}", response_model=ClientSchema)
async def get_client_by_id(org_id: int, client_id: int, db: Session = Depends(get_db)):
    logger.info(f"Get client by id: {client_id}")
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# 🔹 Get all clients for an organization
@router.get("/organizations/{org_id}/clients", response_model=List[ClientSchema])
async def get_clients(org_id: int, db: Session = Depends(get_db)):
    return db.query(Client).filter(Client.organization_id == org_id).all()


# 🔹 Get client by name within an organization
@router.get("/organizations/{org_id}/clients/name/{client_name}", response_model=ClientSchema)
async def get_client_by_name(org_id: int, client_name: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.name == client_name, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


# 🔹 Create a new client under an organization
@router.post("/organizations/{org_id}/clients", response_model=ClientSchema)
async def create_client(org_id: int, client: ClientCreate, db: Session = Depends(get_db)):
    print("📢 Received Client Data:", client.dict())  # ✅ Debugging output
    new_client = Client(
        name=client.name,
        phone=client.phone,
        domain=client.domain,
        creator_id=client.creator_id,  # ✅ Include creator_id if available
        organization_id=org_id  # ✅ Use org_id from the URL
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


# 🔹 Delete a client under an organization
@router.delete("/organizations/{org_id}/clients/{client_id}", response_model=ClientSchema)
async def delete_client(org_id: int, client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return client


# 🔹 Update a client under an organization
@router.patch("/organizations/{org_id}/clients/{client_id}", response_model=ClientSchema)
async def update_client(org_id: int, client_id: int, client: ClientSchema, db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    update_data = client.model_dump(exclude_unset=True)  # ✅ Use model_dump() instead of dict()
    for key, value in update_data.items():
        setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)
    return db_client


# 🔹 Get client stats (Ensure correct schema if needed)
@router.get("/organizations/{org_id}/clients/{client_id}/stats", response_model=ClientSchema)
async def get_client_stats(org_id: int, client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id, Client.organization_id == org_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client
