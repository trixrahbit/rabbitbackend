from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Float, Date
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class TimeEntry(Base):
    __tablename__ = 'time_entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    ticket_id = Column(Integer, ForeignKey('tickets.id'), nullable=True)

    start_time = Column(DateTime, default=func.now(), nullable=False)
    end_time = Column(DateTime, nullable=True)  # No default, updated later
    date = Column(Date, default=func.current_date(), nullable=False)
    hours = Column(Float, nullable=False, default=0.0)  # Default to 0
    description = Column(Text, nullable=True)

    # Relationships
    user = relationship("User", backref="time_entries")
    project = relationship("Project", backref="time_entries")
    task = relationship("Task", backref="time_entries")
    ticket = relationship("Ticket", backref="time_entries")
