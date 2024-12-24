from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db_config.db_connection import Base

class Lead(Base):
    __tablename__ = 'leads'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    source = Column(String)  # Example: Website, Referral, Campaign Name
    status = Column(String)  # Example: New, Contacted, Qualified, Converted, Lost
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    organization_id = Column(Integer, ForeignKey('organizations.id'))

    # Relationships
    campaign = relationship("Campaign", back_populates="leads")
    organization = relationship("Organization", back_populates="leads")
