import logging
import pyodbc
from fastapi import APIRouter
from pydantic_settings import BaseSettings

# Config
class Settings(BaseSettings):
    CLIENT_ID: str
    CLIENT_SECRET: str
    REDIRECT_URI: str
    AUTHORITY: str
    SCOPES: list
    DB_Connection: str
    GITHUB_SECRET_BACKEND: str
    OAUTH_KEY: str


    class Config:
        env_file = "/etc/backend.env"

# Instantiate settings
settings = Settings()

CLIENT_ID = settings.CLIENT_ID
CLIENT_SECRET = settings.CLIENT_SECRET
REDIRECT_URI = settings.REDIRECT_URI
AUTHORITY = settings.AUTHORITY
SCOPES = settings.SCOPES
DB_Connection = settings.DB_Connection

router = APIRouter(prefix="/api")