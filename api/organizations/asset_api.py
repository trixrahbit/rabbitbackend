from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from app.api.user.user_router import get_db
from app.models.models import Organization
from app.schemas.organizations.asset_schema import AssetSchema

router = APIRouter()


@router.get("/{client_id}/{org_id}/assets", response_model=List[AssetSchema])
async def get_assets(client_id: int, org_id: int, db: Session = Depends(get_db)):
    assets = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if assets is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return assets.assets

@router.get("/{client_id}/assets/", response_model=AssetSchema)
async def get_assets(client_id: int, db: Session = Depends(get_db)):
    assets = db.query(Organization).filter(Organization.client_id == client_id).first()
    if assets is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return assets.assets


@router.get("/{client_id}/{org_id}/assets/{asset_id}", response_model=AssetSchema)
async def get_asset(client_id: int, org_id: int, asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset.assets

@router.post("/{client_id}/{org_id}/assets", response_model=AssetSchema)
async def create_asset(client_id: int, org_id: int, asset: AssetSchema, db: Session = Depends(get_db)):
    asset = Organization(**asset.dict())
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return asset

@router.patch("/{client_id}/{org_id}/assets/{asset_id}", response_model=AssetSchema)
async def update_asset(client_id: int, org_id: int, asset_id: int, asset: AssetSchema, db: Session = Depends(get_db)):
    db_asset = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if db_asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    update_data = asset.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_asset, key, value)
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.delete("/{client_id}/{org_id}/assets/{asset_id}", response_model=AssetSchema)
async def delete_asset(client_id: int, org_id: int, asset_id: int, db: Session = Depends(get_db)):
    asset = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.delete(asset)
    db.commit()
    return asset