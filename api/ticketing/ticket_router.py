import logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db_config.db_connection import get_db
from models.clientModel.ticket_model import Ticket
from root.root_elements import router
from schemas.client.ticket_schema import TicketSchema, TicketUpdate, TicketCreate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Get all tickets
@router.get("/tickets", response_model=List[TicketSchema])
async def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(Ticket).all()
    return tickets


# Get a single ticket by ID
@router.get("/tickets/{ticket_id}", response_model=TicketSchema)
async def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket


# Create a new ticket
@router.post("/tickets", response_model=TicketSchema)
async def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    db_ticket = Ticket(**ticket.dict())
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


# Update an existing ticket
@router.put("/tickets/{ticket_id}", response_model=TicketSchema)
async def update_ticket(ticket_id: int, ticket_data: TicketUpdate, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not db_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    for key, value in ticket_data.dict(exclude_unset=True).items():
        setattr(db_ticket, key, value)

    db.commit()
    db.refresh(db_ticket)
    return db_ticket


# Delete a ticket
@router.delete("/tickets/{ticket_id}", response_model=TicketSchema)
async def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()
    return ticket


# Merge multiple tickets
@router.post("/tickets/merge", response_model=TicketSchema)
async def merge_tickets(ticket_ids: List[int], db: Session = Depends(get_db)):
    if len(ticket_ids) < 2:
        raise HTTPException(status_code=400, detail="At least two tickets are required to merge")

    primary_ticket = db.query(Ticket).filter(Ticket.id == ticket_ids[0]).first()
    if not primary_ticket:
        raise HTTPException(status_code=404, detail="Primary ticket not found")

    other_tickets = db.query(Ticket).filter(Ticket.id.in_(ticket_ids[1:])).all()

    for ticket in other_tickets:
        primary_ticket.description += f"\n\n[Merged from Ticket {ticket.id}]\n{ticket.description}"
        db.delete(ticket)

    db.commit()
    return primary_ticket


@router.get("/tickets/{queue_id}", response_model=List[TicketSchema])
async def get_tickets_by_queue(queue_id: int, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.queue_id == queue_id).all()
    return tickets