from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_util import hash_password, verify_access_token, create_access_token
from api.user.user_router import get_db
from models.models import User, Organization
from root.root_elements import router
from schemas.schemas import UserCreate
import re
from fastapi import Query

from services.email.email_service import send_email


@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if not user_data.agree_to_terms:
        raise HTTPException(status_code=400, detail="Must agree to terms and conditions.")

    # ✅ Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email already exists.")

    # ✅ Extract domain from email
    email_domain_match = re.search(r"@([a-zA-Z0-9.-]+)$", user_data.email)
    if not email_domain_match:
        raise HTTPException(status_code=400, detail="Invalid email format.")

    email_domain = email_domain_match.group(1)

    # ✅ Check if organization exists for domain
    existing_organization = db.query(Organization).filter(Organization.domain == email_domain).first()
    if existing_organization:
        raise HTTPException(
            status_code=400,
            detail=f"Your company ({existing_organization.name}) is already registered. Please ask the admin to add you."
        )

    # ✅ Hash the password before saving
    hashed_password = hash_password(user_data.password)

    # ✅ Create user with `is_active=False` (requires email confirmation)
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        is_active=False,
        organization_id=None  # Organization ID is assigned later
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully. Please check your email to confirm your account."}




@router.get("/confirm-email")
async def confirm_email(token: str = Query(...), db: Session = Depends(get_db)):
    payload = verify_access_token(token)  # ✅ Decode token

    if not payload or "email" not in payload:
        raise HTTPException(status_code=400, detail="Invalid or expired token.")

    user = db.query(User).filter(User.email == payload["email"]).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    if user.is_active:
        return {"message": "Your email is already confirmed."}

    # Activate user
    user.is_active = True
    db.commit()

    return {"message": "Email confirmed successfully. You can now log in."}
