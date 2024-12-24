from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    status = Column(String) # e.g., In Progress, Completed
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'))
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'))


    # Relationships
    tasks = relationship("Task", back_populates="project")
    organization = relationship("Organization", back_populates="projects")
    sla_condition = relationship("SLACondition", back_populates="projects")
    billing_agreements = relationship("BillingAgreement", back_populates="project")
    assets = relationship("Asset", back_populates="project")

