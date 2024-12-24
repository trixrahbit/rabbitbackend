from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.auth.auth_util import get_current_user
from app.core.client_create import create_client
from app.models.models import User
from app.schemas.schemas import ClientCreate, ClientSchema

router = APIRouter()


@router.post("/clients/", response_model=ClientSchema)
async def create_client_endpoint(client_data: ClientCreate, db: Session = Depends(get_db),
                                 current_user: User = Depends(get_current_user)):
    # Example permission check (adjust according to your auth system)
    # if not current_user.is_master_tenant:
    #     raise HTTPException(status_code=403, detail="Not authorized to create clients")

    return create_client(db=db, client=client_data, creator_id=current_user.id)