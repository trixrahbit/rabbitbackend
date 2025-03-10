from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from db_config.db_connection import Base
class Campaign(Base):
    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)  # Example: Email, Social Media, Webinar, Event
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Numeric)
    spent = Column(Numeric)
    leads_generated = Column(Integer)
    deals_closed = Column(Integer)
    roi = Column(Numeric)  # Return on Investment
    notes = Column(Text)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    # Relationships
    organization = relationship("Organization", back_populates="campaigns")
    leads = relationship("Lead", back_populates="campaign")
    analytics = relationship("MarketingAnalytics", back_populates="campaign", uselist=False)

