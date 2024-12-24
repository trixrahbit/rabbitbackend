from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from starlette import status

from app import schemas
from app.auth.auth_util import oauth2_scheme, ALGORITHM, SECRET_KEY
from app.db_config.db_connection import database
from app.models import models


def get_current_organization(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        org_id: int = payload.get("org_id")
        if org_id is None:
            raise credentials_exception
        organization = db.query(models.Organization).filter(models.Organization.id == org_id).first()
        if organization is None:
            raise credentials_exception
        return organization
    except JWTError:
        raise credentials_exception
