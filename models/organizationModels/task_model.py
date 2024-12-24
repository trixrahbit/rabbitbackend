from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    status = Column(String) # e.g., Open, In Progress, Closed
    priority = Column(String) # e.g., High, Medium, Low
    due_date = Column(DateTime)
    project_id = Column(Integer, ForeignKey('projects.id'))

    # Relationships
    project = relationship("Project", back_populates="tasks")
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'))
    sla_condition = relationship("SLACondition", back_populates="tasks")
