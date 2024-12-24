from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db_config.db_connection import Base

class AccountReview(Base):
    __tablename__ = 'account_reviews'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    review_date = Column(DateTime, default=func.now())
    notes = Column(Text)
    follow_up_actions = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    creator_id = Column(Integer, ForeignKey('users.id'))
    updated_by_id = Column(Integer, ForeignKey('users.id'))


    # Relationships
    organization = relationship("Organization", back_populates="account_reviews")
    creator = relationship("User", foreign_keys=[creator_id])
    updated_by = relationship("User", foreign_keys=[updated_by_id])

