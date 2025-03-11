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

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime, nullable=True)
    status = Column(String, nullable=False, default="In Progress")  # Example statuses: In Progress, Completed

    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)  # ✅ Fix: Add ForeignKey
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'), nullable=True)
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'), nullable=True)

    # ✅ Relationships
    client = relationship("Client", back_populates="projects")  # ✅ Fix: Add relationship
    organization = relationship("Organization", back_populates="projects")
    sla_condition = relationship("SLACondition", back_populates="projects")
    billing_agreements = relationship("BillingAgreement", back_populates="project")
    assets = relationship("Asset", back_populates="project")

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
