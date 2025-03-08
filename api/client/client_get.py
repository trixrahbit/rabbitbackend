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
@router.get("/clients/", response_model=List[ClientSchema])
async def read_clients(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    clients = db.query(Client).offset(skip).limit(limit).all()
    return clients


# New endpoint to return all clients in JSON format without pagination
@router.get("/get_clients", response_model=List[ClientSchema])
async def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients


# Endpoint to get client ID based on client name
@router.get("/clients/{client_name}/id")
async def get_client_id(client_name: str, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.name == client_name).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"client_id": client.id}


# Endpoint to get organization stats for a client
@router.get("/{client_id}/stats")
async def get_organization_stats(client_id: int, db: Session = Depends(get_db)):
    current_month_start = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_month_start = (current_month_start - timedelta(days=1)).replace(day=1, hour=0, minute=0, second=0,
                                                                         microsecond=0)

    current_count = db.query(Organization).filter(Organization.client_id == client_id,
                                                  Organization.created_at >= current_month_start).count()
    last_month_count = db.query(Organization).filter(Organization.client_id == client_id,
                                                     Organization.created_at < current_month_start,
                                                     Organization.created_at >= last_month_start).count()

    if last_month_count == 0:
        if current_count > 0:
            percentage_change = 100  # Arbitrary large value to indicate significant increase from 0
        else:
            percentage_change = 0  # No change if there are no organizations this month either
    else:
        percentage_change = ((current_count - last_month_count) / last_month_count) * 100

    # Logging for debugging
    logging.info(
        f"Current count: {current_count}, Last month count: {last_month_count}, Percentage change: {percentage_change}%")

    return {"currentCount": current_count, "lastMonthCount": last_month_count, "percentageChange": percentage_change}
