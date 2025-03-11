from sqlalchemy import Column, Integer, ForeignKey, DateTime, func, String
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class SessionsModel(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    token = Column(String)
    start_date = Column(DateTime, default=func.now())
    end_date = Column(DateTime)
    status = Column(String)  # Active, Inactive, Expired, etc.

    # Relationships
    users = relationship("User", back_populates="sessions")