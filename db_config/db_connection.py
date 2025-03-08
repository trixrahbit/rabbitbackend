from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
import pyodbc
from root.root_elements import settings

DATABASE_URL = settings.DB_Connection

# ✅ Use "pyodbc" with proper MSSQL support
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

metadata = MetaData()
Base = declarative_base(metadata=metadata)

# ✅ Use synchronous session for SQLAlchemy operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
