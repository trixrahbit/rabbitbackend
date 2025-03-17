# models/clientModel/queue_model.py
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class Queue(Base):
    __tablename__ = 'queues'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    # Relationship to tickets
    tickets = relationship("Ticket", back_populates="queue")
