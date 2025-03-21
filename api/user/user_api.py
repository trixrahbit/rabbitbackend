import logging
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List

from auth.auth_util import get_current_user
from db_config.db_connection import get_db
from models.models import User, BusinessHours
from root.root_elements import router
from schemas.schemas import UserList, UserUpdateSchema, SessionTimeoutUpdateSchema
from sqlalchemy.orm import joinedload
from passlib.context import CryptContext


@router.get("/organizations/{org_id}/users", response_model=List[UserList])
def read_users_for_organization(org_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching all users for organization {org_id}")
    users = db.query(User).options(joinedload(User.roles)).filter(User.client_id == org_id).all()
    if not users:
        raise HTTPException(status_code=404, detail="No users found for the specified organization")
    return users

@router.delete('/organizations/{org_id}/users/{user_id}')
async def delete_user(org_id: int, user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.patch('/organizations/{org_id}/users/{user_id}')
async def update_user(org_id: int, user_id: int, email: str = None, password: str = None,
                      db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if email:
        user.email = email
    if password:
        user.password = pwd_context.hash(password)
    db.commit()
    return {"message": "User updated successfully"}

@router.get("/organizations/{org_id}/users/{user_id}/profile", response_model=UserList)
def read_user_for_organization(org_id: int, user_id: int, db: Session = Depends(get_db)):
    logging.info(f"Fetching user {user_id} for organization {org_id}")
    user = db.query(User).options(joinedload(User.roles)).filter(User.id == user_id, User.client_id == org_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found for the specified organization")
    return user


@router.put("/users/{user_id}", response_model=UserList)
def update_user(user_id: int, user: UserUpdateSchema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Log the incoming data for debugging
    logging.info(f"Received data for updating user {user_id}: {user.dict(exclude_unset=True)}")

    try:
        # Update basic fields
        for key, value in user.dict(exclude_unset=True, exclude={"business_hours"}).items():
            setattr(db_user, key, value)

        # Handle business hours
        if user.business_hours:
            # Assuming you have a relationship set up for business_hours
            db_user.business_hours.clear()  # Clear existing business hours

            for bh in user.business_hours:
                # Create and add each business hour instance to the user
                if bh.day_of_week:  # Only add if day_of_week is set
                    new_bh = BusinessHours(
                        day_of_week=bh.day_of_week,
                        start_time=bh.start_time,
                        end_time=bh.end_time
                    )
                    db_user.business_hours.append(new_bh)

        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the user")



@router.put("/users/{user_id}/session-timeout")
async def update_session_timeout(
    user_id: int,
    update_data: SessionTimeoutUpdateSchema,  # ✅ Expect data in the request body
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ Allow users to update their session timeout setting. """
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="You do not have permission to modify this user.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if update_data.session_timeout:  # ✅ Update session timeout from request body
        user.session_timeout = update_data.session_timeout
        db.commit()
        db.refresh(user)

    return {"message": "Session timeout updated successfully!", "session_timeout": user.session_timeout}

@router.get("/users/{user_id}/session-timeout")
async def get_session_timeout(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Fetch the session timeout for a given user."""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to access this data.")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    return {"session_timeout": user.session_timeout if user.session_timeout is not None else 30}