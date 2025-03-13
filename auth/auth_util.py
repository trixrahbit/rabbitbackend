import os
import datetime
import jwt  # ✅ Using `pyjwt`
from jwt import ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status
from passlib.context import CryptContext
from api.user.user_router import get_db
from models.models import User, Organization  # ✅ Import Organization model
from root.root_elements import settings

# ✅ Load secret key from settings
SECRET_KEY = settings.OAUTH_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ✅ Password Hashing
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# ✅ Token Creation with Expiry
def create_access_token(data: dict, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    """Generates a JWT token with an expiration time."""
    to_encode = data.copy()
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=expires_delta)
    to_encode.update({"exp": expire})  # ✅ Token expires after defined time
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ✅ Token Verification
def verify_access_token(token: str):
    """Decodes a JWT token and verifies its validity."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # ✅ Contains the original data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


# ✅ Get Current User with `super_admin` from Organization
async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Fetch the authenticated user from the database including their `super_admin` status."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)  # ✅ Reuses verification function
        user_email = payload.get("sub")
        if not user_email:
            raise credentials_exception

        # ✅ Fetch user & join Organization to get `super_admin`
        user = (
            db.query(User)
            .join(Organization, User.organization_id == Organization.id, isouter=True)
            .filter(User.email == user_email)
            .first()
        )

        if not user:
            raise credentials_exception

        # ✅ Extract `super_admin` status
        user_obj = user
        super_admin = user_obj.organization.super_admin if user_obj.organization else False

        user_dict = {
            "id": user_obj.id,
            "name": user_obj.name,
            "email": user_obj.email,
            "organization_id": user_obj.organization_id,
            "super_admin": super_admin,
        }

        return user_dict
    except HTTPException:
        raise credentials_exception
