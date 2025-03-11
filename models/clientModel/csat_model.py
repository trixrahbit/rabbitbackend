from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class Survey(Base):
    __tablename__ = 'surveys'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    sent_date = Column(DateTime, default=func.now())
    response_rate = Column(Numeric)
    organization_id = Column(Integer, ForeignKey('organizations.id'))



    organization = relationship("Organization", back_populates="surveys")
    responses = relationship("SurveyResponse", back_populates="survey")


class SurveyResponse(Base):
    __tablename__ = 'survey_responses'

    id = Column(Integer, primary_key=True)
    response = Column(Text)
    submitted_at = Column(DateTime, default=func.now())
    survey_id = Column(Integer, ForeignKey('surveys.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))
    ticket_id = Column(Integer, ForeignKey('tickets.id'))  # ✅ Explicit FK to Ticket

    # Relationships
    survey = relationship("Survey", back_populates="responses")
    contact = relationship("Contact", back_populates="survey_responses")
    ticket = relationship(
        "Ticket",
        back_populates="survey_responses",
        foreign_keys=[ticket_id]  # ✅ Explicitly specify foreign key to Ticket
    )

