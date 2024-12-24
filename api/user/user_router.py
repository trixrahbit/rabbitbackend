from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.db_config.db_connection import SessionLocal

router = APIRouter()
# Utility function for getting the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


