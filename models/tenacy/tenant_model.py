from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    parent_org_id = Column(Integer, ForeignKey('organizations.id'), nullable=True)

    # Relationship to self to represent parent-child organizations
    children = relationship("Organization", backref='parent', remote_side=[id])

    # Optional: If you have users associated with organizations
    users = relationship("User", back_populates="organization")

