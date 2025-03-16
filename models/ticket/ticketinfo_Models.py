from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from db_config.db_connection import Base


class Priority(Base):
    __tablename__ = 'priorities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tickets = relationship("Ticket", back_populates="priority")  # ✅ Relationship to Tickets
    sla_conditions = relationship("SLACondition", back_populates="priority")


class Impact(Base):
    __tablename__ = 'impacts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tickets = relationship("Ticket", back_populates="impact")  # ✅ Relationship to Tickets
    sla_conditions = relationship("SLACondition", back_populates="impact")


class Status(Base):
    __tablename__ = 'statuses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    tickets = relationship("Ticket", back_populates="status")  # ✅ Relationship to Tickets
