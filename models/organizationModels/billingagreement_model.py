from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base


class BillingAgreement(Base):
    __tablename__ = 'billing_agreements'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    status = Column(String)  # Active, In Maintenance, Decommissioned, etc.
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'))


    # Relationships
    subscriptions = relationship("Subscription", back_populates="billing_agreement")
    organization = relationship("Organization", back_populates="billing_agreements")
    tickets = relationship("Ticket", back_populates="billing_agreement")
    sla_condition = relationship("SLACondition", back_populates="billing_agreements")
    invoices = relationship("Invoice", back_populates="billing_agreement")
    payments = relationship("Payment", back_populates="billing_agreement")
    billing_agreement_items = relationship("BillingAgreementItem", back_populates="billing_agreement")
    project = relationship("Project", back_populates="billing_agreements")
    asset = relationship("Asset", back_populates="billing_agreements")


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
    tickets = relationship("Ticket", back_populates="billing_agreement_item")
    invoices = relationship("Invoice", back_populates="billing_agreement_item")
    payments = relationship("Payment", back_populates="billing_agreement_item")
    project = relationship("Project", back_populates="billing_agreement_item")
    asset = relationship("Asset", back_populates="billing_agreement_item")
    service = relationship("Service", back_populates="billing_agreement_item")



