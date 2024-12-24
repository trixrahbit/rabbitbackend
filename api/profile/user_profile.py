import logging
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.models.models import User
from app.schemas.schemas import UserList
from sqlalchemy.orm import joinedload

router = APIRouter()

@router.get("/organizations/{org_id}/users/{user_id}/profile", response_model=UserList)
def read_user_profile(org_id: int, user_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching user profile for user {user_id}")

    # Query user while eagerly loading roles
    user = db.query(User).options(joinedload(User.roles)).filter(User.client_id == org_id, User.id == user_id).first()

    # If the user is not found, raise an HTTPException
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Transform user and their roles into the schema format expected by the response model
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "username": user.username,
        "roles": [{"id": role.id, "name": role.name} for role in user.roles]
    }

    return user_data