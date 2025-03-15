from fastapi import Depends

from auth.auth_util import get_current_user
from models import User
from root.root_elements import router


@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    """Fetch the profile information of the logged-in user."""
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "organization_id": current_user.organization_id,
        "super_admin": current_user.super_admin,  # ✅ Now correctly derived from organization
    }

