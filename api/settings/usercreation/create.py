from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.auth_util import hash_password, create_access_token
from db_config.db_connection import get_db
from models.models import User, Organization, Client
from root.root_elements import router
from schemas.schemas import UserCreate
import re

from services.email.email_service import send_email


@router.post("/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    if not user_data.agree_to_terms:
        raise HTTPException(status_code=400, detail="Must agree to terms and conditions.")

    # ✅ Extract domain from email
    email_domain_match = re.search(r"@([a-zA-Z0-9.-]+)$", user_data.email)
    if not email_domain_match:
        raise HTTPException(status_code=400, detail="Invalid email format.")

    email_domain = email_domain_match.group(1)

    # ✅ Check if organization already exists
    existing_organization = db.query(Organization).filter(Organization.domain == email_domain).first()

    if existing_organization:
        raise HTTPException(
            status_code=400,
            detail=f"Your company ({existing_organization.name}) is already registered. Please ask the admin to add you."
        )

    # ✅ Create a new Organization with the provided company name
    new_organization = Organization(
        name=user_data.company_name,  # ✅ Use provided company name
        domain=email_domain,
        super_admin=False  # ❌ Organization itself should not be super admin
    )
    db.add(new_organization)
    db.commit()
    db.refresh(new_organization)

    # ✅ Ensure a default Client exists, copying the domain from the organization
    existing_client = db.query(Client).filter(Client.organization_id == new_organization.id).first()
    if not existing_client:
        new_client = Client(
            name=user_data.company_name,  # ✅ Use company name for the client
            domain=email_domain,  # ✅ Copy domain
            organization_id=new_organization.id
        )
        db.add(new_client)
        db.commit()
        db.refresh(new_client)

    # ✅ Create User and assign them to the new Organization as a Super Admin
    hashed_password = hash_password(user_data.password)
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        hashed_password=hashed_password,
        organization_id=new_organization.id,  # ✅ Assign user to their new organization
        agree_to_terms=user_data.agree_to_terms,
        is_active=False,  # ✅ User must verify email before activation
        is_superuser=True  # ✅ First user is super admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # ✅ Generate email confirmation token
    token = create_access_token({"sub": db_user.email})

    # ✅ Send confirmation email
    send_confirmation_email(db_user.email, db_user.name, token)

    return {"message": "User registered successfully. Please check your email to verify your account."}


def send_confirmation_email(to_email: str, name: str, token: str):
    confirmation_link = f"https://app.webitservices.com/confirm-email?token={token}"

    email_body = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Confirm Your Email</title>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; }}
            .container {{ max-width: 480px; margin: 40px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }}
            .header {{ font-size: 20px; font-weight: bold; color: #333; margin-bottom: 15px; }}
            .content {{ font-size: 16px; color: #555; line-height: 1.6; }}
            .button {{ display: inline-block; background-color: #007BFF; color: white; padding: 12px 20px; border-radius: 5px; text-decoration: none; font-weight: bold; margin-top: 20px; }}
            .footer {{ font-size: 12px; color: #888; margin-top: 20px; }}
        </style>
    </head>
    <body>
    <div class="container">
        <div class="header">Confirm Your Email Address</div>
        <div class="content">
            <p>Hello <strong>{name}</strong>,</p>
            <p>Thank you for signing up! Please confirm your email address by clicking the button below:</p>
            <a href="{confirmation_link}" class="button">Confirm Email</a>
            <p>If you didn’t sign up, please ignore this email.</p>
        </div>
        <div class="footer">© 2025 WEBIT Services. All rights reserved.</div>
    </div>
    </body>
    </html>
    """

    send_email(to_email, "Confirm Your Email", email_body, html=True)