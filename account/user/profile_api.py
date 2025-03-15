from fastapi import Depends

from auth.auth_util import get_current_user
from models import User
from root.root_elements import router


@router.get("/profile")
async def get_user_profile(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "mobile": current_user.mobile,
        "location": current_user.location,
        "organization": {"name": current_user.organization.name} if current_user.organization else None,
    }
