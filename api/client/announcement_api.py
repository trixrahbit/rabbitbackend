from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.clientModel.announcement_model import Announcement
from schemas.client.announcement_schema import AnnouncementSchema

router = APIRouter()

@router.get("/{client_id}/{org_id}/announcements", response_model=List[AnnouncementSchema])
async def get_announcements(client_id: int, org_id: int, db: Session = Depends(get_db)):
    return db.query(Announcement).filter(Announcement.client_id == client_id, Announcement.org_id == org_id).all()


@router.get("/{client_id}/announcements/{announcement_id}", response_model=AnnouncementSchema)
async def get_announcement(client_id: int, org_id: int, announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id, Announcement.client_id == client_id, Announcement.org_id == org_id).first()
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement


@router.get("/{client_id}/{org_id}/announcements/{announcement_id}", response_model=AnnouncementSchema)
async def get_announcement(client_id: int, org_id: int, announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id, Announcement.client_id == client_id, Announcement.org_id == org_id).first()
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    return db_announcement

@router.post("/{client_id}/{org_id}/announcements", response_model=AnnouncementSchema)
async def create_announcement(client_id: int, org_id: int, announcement: AnnouncementSchema, db: Session = Depends(get_db)):
    db_announcement = Announcement(**announcement.dict(), client_id=client_id, org_id=org_id)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.patch("/{client_id}/{org_id}/announcements/{announcement_id}", response_model=AnnouncementSchema)
async def update_announcement(client_id: int, org_id: int, announcement_id: int, announcement: AnnouncementSchema, db: Session = Depends(get_db)):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id, Announcement.client_id == client_id, Announcement.org_id == org_id).first()
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    update_data = announcement.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_announcement, key, value)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

@router.delete("/{client_id}/{org_id}/announcements/{announcement_id}", response_model=AnnouncementSchema)
async def delete_announcement(client_id: int, org_id: int, announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id, Announcement.client_id == client_id, Announcement.org_id == org_id).first()
    if db_announcement is None:
        raise HTTPException(status_code=404, detail="Announcement not found")
    db.delete(db_announcement)
    db.commit()
    return db_announcement