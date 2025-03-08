# database/db_connection.py
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import urllib
from root.root_elements import settings

# Convert DB_Connection string for SQLAlchemy compatibility
params = urllib.parse.quote_plus(settings.DB_Connection)
DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Create SQLAlchemy async engine
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    fast_executemany=True
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

# Declarative base
Base = declarative_base()
