from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.api.user.user_router import get_db
from app.models.models import Role, ClientRole
from app.schemas.schemas import RoleSchema, RoleCreateSchema

router = APIRouter()

@router.get("/organizations/{org_id}/roles", response_model=List[RoleSchema])
async def get_roles_for_organization(org_id: int, db: Session = Depends(get_db)):
    # Ensure this subquery is correctly formulated
    subquery = db.query(ClientRole.role_id).filter(ClientRole.organization_id == org_id).subquery()
    roles = db.query(Role).filter(
        (Role.default == True) | (Role.id.in_(subquery))
    ).distinct().all()

    if not roles:
        raise HTTPException(status_code=404, detail="Roles not found for the specified organization.")

    return roles

@router.post("/organizations/{org_id}/roles", response_model=RoleSchema)
async def create_role_for_organization(org_id: int, role_data: RoleCreateSchema, db: Session = Depends(get_db)):
    print("Received role data:", jsonable_encoder(role_data))

    # Create a new Role instance
    new_role = Role(name=role_data.name, default=role_data.is_default)
    db.add(new_role)
    db.commit()
    db.refresh(new_role)

    # If the role is not marked as default, associate it with the given organization
    if not role_data.is_default:
        new_client_role = ClientRole(role_id=new_role.id, organization_id=org_id)
        db.add(new_client_role)
        db.commit()

    return new_role


# DELETE endpoint
@router.delete("/roles/{role_id}", response_model=Any)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(role)
    db.commit()
    return {"ok": True}

# PATCH endpoint
@router.patch("/roles/{role_id}", response_model=Any)
def update_role(role_id: int, name: str = Body(...), db: Session = Depends(get_db)):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    role.name = name
    db.commit()
    return role