# # database/db_connection.py
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from root.root_elements import settings

DATABASE_URL = settings.DB_Connection

# SQLAlchemy specific
engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Databases library specific
database = Database(DATABASE_URL)

# For synchronous operations if needed, like migrations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
