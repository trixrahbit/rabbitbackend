from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db_config.db_connection import Base

class StrategicObjective(Base):
    __tablename__ = 'strategic_objectives'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    objective = Column(Text)
    target_completion_date = Column(DateTime)
    status = Column(String)  # Example: Not Started, In Progress, Completed

    # Relationships
    organization = relationship("Organization", back_populates="strategic_objectives")

