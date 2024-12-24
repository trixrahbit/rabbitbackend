from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.db_config.db_connection import Base


class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    name = Column(String)
    address = Column(String)
    phone = Column(String)

    # Relationships
    organization = relationship("Organization", back_populates="locations")

