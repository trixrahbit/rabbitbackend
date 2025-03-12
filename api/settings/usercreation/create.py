from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_util import hash_password
from api.user.user_router import get_db
from models.models import User, Organization
from root.root_elements import router
from schemas.schemas import UserCreate
import re

@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if not user_data.agree_to_terms:
        raise HTTPException(status_code=400, detail="Must agree to terms and conditions.")

    # Extract the domain from the email
    email_domain_match = re.search(r"@([a-zA-Z0-9.-]+)$", user_data.email)
    if not email_domain_match:
        raise HTTPException(status_code=400, detail="Invalid email format.")

    email_domain = email_domain_match.group(1)

    # Check if the domain already exists in the organizations table
    existing_organization = db.query(Organization).filter(Organization.domain == email_domain).first()
    if existing_organization:
        raise HTTPException(
            status_code=400,
            detail=f"Your company ({existing_organization.name}) is already registered. Please ask the admin to add you."
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user without an assigned organization
    db_user = UserCreate(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        agree_to_terms=user_data.agree_to_terms,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully."}



