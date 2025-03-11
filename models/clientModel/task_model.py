from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Enum
from sqlalchemy.orm import relationship
import enum
from db_config.db_connection import Base

# Define Enums for Status and Priority
class TaskStatus(enum.Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    CLOSED = "Closed"

class TaskPriority(enum.Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.OPEN)
    priority = Column(Enum(TaskPriority), nullable=False, default=TaskPriority.MEDIUM)
    due_date = Column(DateTime, nullable=True)

    # Foreign Keys
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    sla_condition_id = Column(Integer, ForeignKey('sla_conditions.id'), nullable=True)

    # Relationships
    project = relationship("Project", back_populates="tasks")
    sla_condition = relationship("SLACondition", back_populates="tasks")

