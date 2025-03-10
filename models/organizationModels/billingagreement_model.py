from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from models import Base


class BillingAgreement(Base):
    __tablename__ = 'billing_agreements'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    status = Column(String, nullable=True)
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'), nullable=True)

    client = relationship("Client", back_populates="billing_agreements")
    sla_condition = relationship("SLACondition")
    tickets = relationship("Ticket", back_populates="billing_agreement")
    billing_agreement_items = relationship("BillingAgreementItem", back_populates="billing_agreement")


class BillingAgreementItem(Base):
    __tablename__ = 'billing_agreement_items'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    quantity = Column(Integer)
    price = Column(Numeric)
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'))
    status = Column(String)  # Active, In Maintenance, Decommissioned, etc.

    # Relationships
    billing_agreement = relationship("BillingAgreement", back_populates="billing_agreement_items")
    # invoices = relationship("Invoice", back_populates="billing_agreement_item")
    # payments = relationship("Payment", back_populates="billing_agreement_item")
    # project = relationship("Project", back_populates="billing_agreement_item")
    # asset = relationship("Asset", back_populates="billing_agreement_item")
    # service = relationship("Service", back_populates="billing_agreement_item")



