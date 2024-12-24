from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from app.models import Base

class Checklist(Base):
    __tablename__ = "checklists"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    story_id = Column(Integer, ForeignKey("stories.id", ondelete="CASCADE"), nullable=True)
    name = Column(String, nullable=False)  # New column for checklist name
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("ChecklistItem", back_populates="checklist", cascade="all, delete-orphan")

class ChecklistItem(Base):
    __tablename__ = "checklist_items"

    id = Column(Integer, primary_key=True, index=True)
    checklist_id = Column(Integer, ForeignKey("checklists.id", ondelete="CASCADE"))
    description = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    completed_by = Column(String, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    order = Column(Integer, nullable=False, default=0)  # New column for item order

    checklist = relationship("Checklist", back_populates="items")
