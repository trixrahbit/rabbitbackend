from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from db_config.db_connection import Base
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
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)
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

    # Relationships

    billing_agreement = relationship("BillingAgreement", backref="tickets", lazy="joined")
    organization = relationship("Organization", back_populates="tickets")
    contact = relationship("Contact", back_populates="tickets")
    survey_responses = relationship("SurveyResponse", backref="tickets", lazy="joined")
    sla_condition = relationship("SLACondition", backref="tickets", lazy="joined")
