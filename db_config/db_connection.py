# # database/db_connection.py
from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:312Bakersfield!@localhost/rabbitpsa"

# SQLAlchemy specific
engine = create_engine(DATABASE_URL)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Databases library specific
database = Database(DATABASE_URL)

# For synchronous operations if needed, like migrations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
