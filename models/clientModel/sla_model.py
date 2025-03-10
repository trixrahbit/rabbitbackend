from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from models import Base

class SLACondition(Base):
    __tablename__ = 'sla_conditions'

    id = Column(Integer, primary_key=True)
    sla_policy_id = Column(Integer, ForeignKey('sla_policies.id'))
    priority_id = Column(Integer, ForeignKey('priorities.id'))
    impact_id = Column(Integer, ForeignKey('impacts.id'))
    response_time = Column(Integer)
    resolution_time = Column(Integer)

    sla_policy = relationship("SLA", back_populates="conditions")
    priority = relationship("Priority", back_populates="sla_conditions")
    impact = relationship("Impact", back_populates="sla_conditions")
    billing_agreements = relationship("BillingAgreement", back_populates="sla_condition")
    tickets = relationship("Ticket", back_populates="sla_condition")

class SLA(Base):
    __tablename__ = 'sla_policies'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)


class Priority(Base):
    __tablename__ = 'priorities'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    level = Column(Integer, nullable=False)  # Higher numbers mean higher priority
    description = Column(String, nullable=True)


class Impact(Base):
    __tablename__ = 'impacts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    level = Column(Integer, nullable=False)  # Higher numbers mean greater impact
    description = Column(String, nullable=True)




