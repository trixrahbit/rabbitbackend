import logging

from sqlalchemy.orm import Session

from models.models import Client
from schemas.schemas import ClientCreate


def create_client(db: Session, client: ClientCreate, creator_id: int):
    db_client = Client(
        name=client.name,
        email=client.email,
        phone=client.phone,
        creator_id=creator_id
    )
    logging.info(f"Creating client: {db_client}")
    db.add(db_client)
    logging.info(f"Client created: {db_client}")
    db.commit()
    logging.info(f"Client committed: {db_client}")
    db.refresh(db_client)
    return db_client
