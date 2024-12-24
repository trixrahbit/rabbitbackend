from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from models import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    methodology = Column(String, nullable=False)

    # Relationships will be defined later
    phases = relationship("Phase", back_populates="project")
    tasks = relationship("Task", back_populates="project")
    sprints = relationship("Sprint", back_populates="project")
    stories = relationship("Story", back_populates="project")


class Phase(Base):
    __tablename__ = "phases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))

    # Relationships
    project = relationship("Project", back_populates="phases")
    tasks = relationship("Task", back_populates="phase")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    phase_id = Column(Integer, ForeignKey("phases.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))

    # Relationships
    phase = relationship("Phase", back_populates="tasks")
    project = relationship("Project", back_populates="tasks")


class Sprint(Base):
    __tablename__ = "sprints"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))

    # Relationships
    project = relationship("Project", back_populates="sprints")
    stories = relationship("Story", back_populates="sprint")


class Story(Base):
    __tablename__ = "stories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    sprint_id = Column(Integer, ForeignKey("sprints.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"))

    # Relationships
    sprint = relationship("Sprint", back_populates="stories")
    project = relationship("Project", back_populates="stories")
