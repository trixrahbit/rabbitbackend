from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base


class SLA(Base):
    __tablename__ = 'sla_policies'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)


class Priority(Base):
    __tablename__ = 'priorities'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    level = Column(Integer)  # Higher numbers mean higher priority
    description = Column(String)


class Impact(Base):
    __tablename__ = 'impacts'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    level = Column(Integer)  # Higher numbers mean greater impact
    description = Column(String)


class SLACondition(Base):
    __tablename__ = 'sla_conditions'
    id = Column(Integer, primary_key=True)
    sla_policy_id = Column(Integer, ForeignKey('sla_policies.id'))
    priority_id = Column(Integer, ForeignKey('priorities.id'))
    impact_id = Column(Integer, ForeignKey('impacts.id'))
    response_time = Column(Integer)  # Time in hours/minutes
    resolution_time = Column(Integer)  # Time in hours/minutes

    sla_policy = relationship("SLAPolicy", backref="conditions")
    priority = relationship("Priority", backref="sla_conditions")
    impact = relationship("Impact", backref="sla_conditions")
    projects = relationship("Project", back_populates="sla_condition")
    tasks = relationship("Task", back_populates="sla_condition")
    tickets = relationship("Ticket", back_populates="sla_condition")
