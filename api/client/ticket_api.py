from fastapi import Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.clientModel.ticket_model import Ticket
from root.root_elements import router
from schemas.client.ticket_schema import TicketSchema


@router.get("/{client_id}/tickets", response_model=List[TicketSchema])
async def get_tickets(client_id: int, db: Session = Depends(get_db)):
    tickets = db.query(Ticket).filter(Ticket.client_id == client_id).all()
    return tickets

@router.get("/{client_id}/tickets/{ticket_id}", response_model=TicketSchema)
async def get_ticket(client_id: int, ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.client_id == client_id, Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.get("/{client_id}/{org_id}/tickets/{ticket_id}", response_model=TicketSchema)
async def get_ticket(client_id: int, org_id: int, ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(Ticket).filter(Ticket.client_id == client_id, Ticket.org_id == org_id, Ticket.id == ticket_id).first()
    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

@router.post("/{client_id}/tickets", response_model=TicketSchema)
async def create_ticket(client_id: int, ticket: TicketSchema, db: Session = Depends(get_db)):
    db_ticket = Ticket(**ticket.dict(), client_id=client_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.patch("/{client_id}/tickets/{ticket_id}", response_model=TicketSchema)
async def update_ticket(client_id: int, ticket_id: int, ticket: TicketSchema, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.client_id == client_id, Ticket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    update_data = ticket.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

@router.delete("/{client_id}/tickets/{ticket_id}", response_model=TicketSchema)
async def delete_ticket(client_id: int, ticket_id: int, db: Session = Depends(get_db)):
    db_ticket = db.query(Ticket).filter(Ticket.client_id == client_id, Ticket.id == ticket_id).first()
    if db_ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    db.delete(db_ticket)
    db.commit()
    return db_ticket