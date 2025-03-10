from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db_config.db_connection import Base

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


class SLACondition(Base):
    __tablename__ = 'sla_conditions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    sla_policy_id = Column(Integer, ForeignKey('sla_policies.id'), nullable=False)
    priority_id = Column(Integer, ForeignKey('priorities.id'), nullable=False)
    impact_id = Column(Integer, ForeignKey('impacts.id'), nullable=False)
    response_time = Column(Integer, nullable=False)  # Time in hours/minutes
    resolution_time = Column(Integer, nullable=False)  # Time in hours/minutes

    # Relationships
    sla_policy = relationship("SLA", backref="conditions")
    priority = relationship("Priority", backref="sla_conditions")
    impact = relationship("Impact", backref="sla_conditions")

    # Ensure these exist in related models
    tickets = relationship("Ticket", back_populates="sla_condition", cascade="all, delete-orphan")
