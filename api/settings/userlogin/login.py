import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from api.user.user_router import get_db
from auth.auth_util import create_access_token, verify_password
from models.models import User, Client

router = APIRouter(prefix="/api")

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logging.info(f"Logging in user {form_data.username}")
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Fetch the client object using client_id from the user
    client = db.query(Client).filter(Client.id == user.client_id).first() if user.client_id else None

    access_token = create_access_token(data={"sub": user.email})
    logging.info(f"User {user.email} logged in successfully with token {access_token}")

    # Ensure you're referencing client attributes correctly
    user_info = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "organization": {
            "id": client.id if client else None,
            "name": client.name if client else "No Organization",
        }
    }
    return {"access_token": access_token, "token_type": "bearer", "user": user_info}