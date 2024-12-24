from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db_config.db_connection import Base


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    role = Column(String) # e.g., IT Manager, Support Engineer
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    # Relationships
    organization = relationship("Organization", back_populates="contacts")
    survey_responses = relationship("SurveyResponse", back_populates="contact")
    tickets = relationship("Ticket", back_populates="contact")
    leads = relationship("Lead", back_populates="contact")

