from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from models import Base


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)  # Ensure uniqueness
    phone = Column(String(20), nullable=True)
    role = Column(String(100), nullable=True)  # Ensuring a reasonable max length
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)

    # Relationships
    organization = relationship("Organization", back_populates="contacts")
    survey_responses = relationship("SurveyResponse", back_populates="contact")
    tickets = relationship("Ticket", back_populates="contact")
    leads = relationship("Lead", back_populates="contact")

