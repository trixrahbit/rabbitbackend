from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db_config.db_connection import Base


class IncidentReport(Base):
    __tablename__ = 'incident_reports'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)
    priority = Column(String) # e.g., Low, Medium, High
    status = Column(String) # e.g., Open, In Progress, Resolved
    opened_at = Column(DateTime, default=func.now())
    closed_at = Column(DateTime, nullable=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    # Relationships
    organization = relationship("Organization", back_populates="incident_reports")
