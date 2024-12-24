from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from db_config.db_connection import Base

class KnowledgeBaseArticle(Base):
    __tablename__ = 'knowledge_base_articles'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    author_id = Column(Integer, ForeignKey('users.id'))
    tags = Column(String)  # Could be a comma-separated list or a relationship to a Tags table

    # Relationships
    author = relationship("User", backref="articles")
