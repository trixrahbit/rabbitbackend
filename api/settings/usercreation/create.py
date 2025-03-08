from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_util import hash_password
from api.user.user_router import get_db
from models.models import User
from root.root_elements import router
from schemas.schemas import UserCreate

@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if not user_data.agree_to_terms:
        raise HTTPException(status_code=400, detail="Must agree to terms and conditions.")

    hashed_password = hash_password(user_data.password)

    # Ensure that 'agree_to_terms' is included when creating the User object
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        agree_to_terms=user_data.agree_to_terms  # Include this field
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully."}


