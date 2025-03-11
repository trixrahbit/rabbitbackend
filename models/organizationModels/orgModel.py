from sqlalchemy import Column, Integer, String
from db_config.db_connection import Base


class OrganizationType(Base):
    __tablename__ = 'organization_types'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class Industry(Base):
    __tablename__ = 'industries'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class OrganizationSize(Base):
    __tablename__ = 'organization_sizes'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)