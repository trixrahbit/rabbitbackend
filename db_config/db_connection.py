from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from root.root_elements import settings

DATABASE_URL = settings.DB_Connection

# ✅ Use "pyodbc" with proper MSSQL support
engine = create_engine(
    DATABASE_URL,
    pool_size=10,  # ✅ Maintain up to 10 active connections
    max_overflow=20,  # ✅ Allow 20 extra connections if needed
    pool_pre_ping=True,  # ✅ Checks if connection is still alive before using it
    connect_args={"check_same_thread": False}
)
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# ✅ Use synchronous session for SQLAlchemy operations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


