from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id = Column(Integer, primary_key=True)
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'))
    billing_agreement_item_id = Column(Integer, ForeignKey('billing_agreement_items.id'))
    service_id = Column(Integer, ForeignKey('services.id'))
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    status = Column(String)  # Active, Suspended, Cancelled

    # Relationships
    billing_agreement = relationship("BillingAgreement", back_populates="subscriptions")
    billing_agreement_item = relationship("BillingAgreementItem", back_populates="subscriptions")
    service = relationship("Service", back_populates="subscriptions")

