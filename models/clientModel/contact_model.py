from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_config.db_connection import Base

class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)  # Ensure uniqueness
    phone = Column(String(20), nullable=True)
    role = Column(String(100), nullable=True)  # Ensuring a reasonable max length
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)

    # ✅ Relationship to Client
    client = relationship("Client", back_populates="contacts")

    # ✅ Fix: Ensure SurveyResponse is fully defined before referencing it
    survey_responses = relationship("SurveyResponse", back_populates="contact")

    tickets = relationship("Ticket", back_populates="contact")
    # leads = relationship("Lead", back_populates="contact")
