from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from db_config.db_connection import Base


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    methodology = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    phases = relationship("TemplatePhase", back_populates="template", cascade="all, delete-orphan")
    tasks = relationship("TemplateTask", back_populates="template", cascade="all, delete-orphan")
    sprints = relationship("TemplateSprint", back_populates="template", cascade="all, delete-orphan")
    stories = relationship("TemplateStory", back_populates="template", cascade="all, delete-orphan")

class TemplatePhase(Base):
    __tablename__ = "template_phases"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    template_id = Column(Integer, ForeignKey('templates.id'))

    template = relationship("Template", back_populates="phases")
    tasks = relationship("TemplateTask", back_populates="phase", cascade="all, delete-orphan")

class TemplateTask(Base):
    __tablename__ = "template_tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    phase_id = Column(Integer, ForeignKey('template_phases.id'))
    template_id = Column(Integer, ForeignKey('templates.id'))

    phase = relationship("TemplatePhase", back_populates="tasks")
    template = relationship("Template", back_populates="tasks")

class TemplateSprint(Base):
    __tablename__ = "template_sprints"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    template_id = Column(Integer, ForeignKey('templates.id'))

    template = relationship("Template", back_populates="sprints")
    stories = relationship("TemplateStory", back_populates="sprint", cascade="all, delete-orphan")

class TemplateStory(Base):
    __tablename__ = "template_stories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    budget_hours = Column(Float, nullable=True)
    sprint_id = Column(Integer, ForeignKey('template_sprints.id'))
    template_id = Column(Integer, ForeignKey('templates.id'))

    sprint = relationship("TemplateSprint", back_populates="stories")
    template = relationship("Template", back_populates="stories")
