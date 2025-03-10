from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
import enum

from db_config.db_connection import Base

# Define Enum for Project Status
class ProjectStatus(enum.Enum):
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"

class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, default=func.now(), nullable=False)
    end_date = Column(DateTime, nullable=True)
    status = Column(Enum(ProjectStatus), nullable=False, default=ProjectStatus.IN_PROGRESS)

    # Foreign Keys
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'), nullable=True)
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'), nullable=True)

    # Relationships
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    organization = relationship("Organization", back_populates="projects")
    sla_condition = relationship("SLACondition", back_populates="projects")
    billing_agreements = relationship("BillingAgreement", back_populates="project")
    assets = relationship("Asset", back_populates="project")
