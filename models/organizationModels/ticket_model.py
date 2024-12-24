from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base

class Ticket(Base):
    __tablename__ = 'tickets'
    id = Column(Integer, primary_key=True)
    subject = Column(String)
    description = Column(Text)
    status = Column(String) # e.g., Open, Resolved
    priority = Column(String)
    impact = Column(String)
    created_at = Column(DateTime, default=func.now())
    resolved_at = Column(DateTime)
    sla_id = Column(Integer, ForeignKey('slas.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'))
    contact_id = Column(Integer, ForeignKey('contacts.id'))


    # Relationships
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'))
    sla_condition = relationship("SLACondition", back_populates="tickets")
    billing_agreement = relationship("BillingAgreement", back_populates="tickets")
    organization = relationship("Organization", back_populates="tickets")
    contact = relationship("Contact", back_populates="tickets")
    survey_responses = relationship("SurveyResponse", back_populates="ticket")

