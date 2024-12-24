from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Numeric
from sqlalchemy.orm import relationship

from db_config.db_connection import Base


class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    monthly_cost = Column(Numeric)  # The cost could be a fixed amount or vary based on usage

    # Relationships
    subscriptions = relationship("Subscription", back_populates="service")

