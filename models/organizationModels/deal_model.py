from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base


class Deal(Base):
    __tablename__ = 'deals'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    value = Column(Numeric)
    stage = Column(String)  # Example: Prospect, Proposal, Negotiation, Won, Lost
    expected_close_date = Column(DateTime)
    actual_close_date = Column(DateTime, nullable=True)


    # Relationships
    organization = relationship("Organization", back_populates="deals")
