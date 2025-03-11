from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db_config.db_connection import Base

class ITAssessment(Base):
    __tablename__ = 'it_assessments'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    assessment_date = Column(DateTime, default=func.now())
    summary = Column(Text)
    detailed_findings = Column(Text)
    recommendations = Column(Text)

    # Relationships
    organization = relationship("Organization", back_populates="it_assessments")
