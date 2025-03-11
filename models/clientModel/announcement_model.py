from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class Announcement(Base):
    __tablename__ = 'announcements'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organization = relationship("Organization", back_populates="announcements")
