from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from db_config.db_connection import Base

class MarketingAnalytics(Base):
    __tablename__ = 'marketing_analytics'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    impressions = Column(Integer)
    clicks = Column(Integer)
    conversions = Column(Integer)
    conversion_rate = Column(Numeric)
    cost_per_click = Column(Numeric)
    cost_per_conversion = Column(Numeric)

    # Relationships
    campaign = relationship("Campaign", back_populates="analytics")
