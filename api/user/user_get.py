import logging
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from db_config.db_connection import get_db
from models.models import User
from root.root_elements import router
from schemas.schemas import UserList
from sqlalchemy.orm import joinedload


@router.get("/organizations/{org_id}/users", response_model=List[UserList])
def read_users_for_organization(org_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching all users for organization {org_id}")

    # Query users while eagerly loading roles
    users = db.query(User).options(joinedload(User.roles)).filter(User.organization_id == org_id).all()

    # If the users list is empty, it means no users were found for that organization
    if not users:
        raise HTTPException(status_code=404, detail="No users found for the specified organization")

    # Transform users and their roles into the schema format expected by the response model
    users_data = [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "username": user.username,
            "roles": [{"id": role.id, "name": role.name} for role in user.roles]
        } for user in users
    ]

    return users_data
