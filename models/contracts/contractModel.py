from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_number = Column(String(255), nullable=False, unique=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    details = Column(Text, nullable=True)

    # Relationships (adjust as needed)
    client = relationship("Client", back_populates="contracts")
    tickets = relationship("Ticket", back_populates="contracts")
