from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

from models import Base


class Ticket(Base):
    __tablename__ = 'tickets'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Ticket Details
    title = Column(String(500), nullable=False)
    subject = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)

    # Status and Priorities
    status = Column(Integer, nullable=False, default=1)  # Open by default
    priority = Column(Integer, nullable=False, default=3)  # Default to Medium
    impact = Column(Integer, nullable=False, default=1)  # Default to Low

    # Dates
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    last_activity_date = Column(DateTime, nullable=True)

    # Foreign Keys
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)  # ✅ Fix: Attach to Client
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'), nullable=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=True)

    # SLA and Queue
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'), nullable=True)
    queue_id = Column(Integer, ForeignKey('queues.id'), nullable=True)

    # SLA compliance tracking
    service_level_agreement_met = Column(Boolean, nullable=False, default=False)

    # Other Identifiers
    ticket_number = Column(String(255), nullable=False, unique=True)
    ticket_type = Column(Integer, nullable=True)
    ticket_category = Column(Integer, nullable=True)

    survey_id = Column(Integer, ForeignKey('survey_responses.id'), nullable=True)

    # ✅ Fix Relationship for BillingAgreement
    billing_agreement = relationship("BillingAgreement", back_populates="tickets")
    client = relationship("Client", back_populates="tickets")  # ✅ Fix: Attach to Client
    contact = relationship("Contact", back_populates="tickets")
    sla_condition = relationship("SLACondition", back_populates="tickets")
    survey_responses = relationship("SurveyResponse", back_populates="tickets")
