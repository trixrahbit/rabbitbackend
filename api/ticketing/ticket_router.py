# app/api/ticket_router.py
import logging

from fastapi import APIRouter
from typing import List

from schemas.organizations.ticket_schema import TicketSchema

router = APIRouter()

# Sample data for demonstration
tickets = [
    {"id": 1, "title": "Bug in homepage", "description": "There's a bug in the homepage when you click the button"},
    {"id": 2, "title": "New feature request", "description": "Can we have a new feature that does X?"},
    {"id": 3, "title": "Performance issues", "description": "The application is slow when accessing the settings page."},
]


@router.get("/tickets", response_model=List[TicketSchema])
async def get_tickets():
    logging.info(f"Fetching all tickets {tickets}")
    return tickets

