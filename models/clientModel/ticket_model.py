from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from db_config.db_connection import Base

class Ticket(Base):
    __tablename__ = 'tickets'

    # Primary Key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Ticket Details
    title = Column(String(500), nullable=False)
    subject = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)

    # Status, Priority, and Impact as Foreign Keys
    status_id = Column(Integer, ForeignKey('statuses.id'), nullable=False)
    priority_id = Column(Integer, ForeignKey('priorities.id'), nullable=False)
    impact_id = Column(Integer, ForeignKey('impacts.id'), nullable=False)

    # Dates
    created_at = Column(DateTime, server_default=func.now())
    resolved_at = Column(DateTime, nullable=True)
    due_date = Column(DateTime, nullable=True)
    last_activity_date = Column(DateTime, nullable=True)

    # Foreign Keys
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'), nullable=True)
    contact_id = Column(Integer, ForeignKey('contacts.id'), nullable=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=True)

    # SLA and Queue
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'), nullable=True)
    queue_id = Column(Integer, ForeignKey('queues.id'), nullable=True)

    # NEW: Organization association
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)

    # SLA compliance tracking
    service_level_agreement_met = Column(Boolean, nullable=False, default=False)

    # Other Identifiers
    ticket_number = Column(String(255), nullable=False, unique=True)
    ticket_type = Column(Integer, nullable=True)
    ticket_category = Column(Integer, nullable=True)

    # Relationships
    client = relationship("Client", back_populates="tickets")
    billing_agreement = relationship("BillingAgreement", back_populates="tickets")
    contact = relationship("Contact", back_populates="tickets")
    sla_condition = relationship("SLACondition", back_populates="tickets")
    priority = relationship("Priority", back_populates="tickets")
    impact = relationship("Impact", back_populates="tickets")
    status = relationship("Status", back_populates="tickets")
    queue = relationship("Queue", back_populates="tickets")  # NEW relationship
    survey_responses = relationship("SurveyResponse", back_populates="ticket")
    contracts= relationship("Contract", back_populates="tickets")