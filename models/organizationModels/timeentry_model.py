from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Float, Numeric, Date
from sqlalchemy.orm import relationship

from db_config.db_connection import Base

class TimeEntry(Base):
    __tablename__ = 'time_entries'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey('users.id'))
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=True)
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime, default=func.now())
    date = Column(Date)
    hours = Column(Numeric)
    description = Column(Text)

    # Relationships
    user = relationship("User", backref="time_entries")
    project = relationship("Project", backref="time_entries")
    task = relationship("Task", backref="time_entries")
    ticket = relationship("Ticket", backref="time_entries")


