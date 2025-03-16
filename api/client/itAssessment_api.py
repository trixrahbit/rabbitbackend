import logging

from fastapi import Depends, HTTPException
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db_config.db_connection import get_db
from models.models import Organization
from root.root_elements import router
from schemas.client.itAssessment_schema import ItAssessmentSchema


@router.get("/{client_id}/itAssessment", response_model=List[ItAssessmentSchema])
async def read_it_assessments(client_id: int, db: Session = Depends(get_db)):
    it_assessments = db.query(Organization).filter(Organization.client_id == client_id).all
    return it_assessments

@router.get("/{client_id}/itAssessment/{it_assessment_id}", response_model=ItAssessmentSchema)
async def read_it_assessment(it_assessment_id: int, db: Session = Depends(get_db)):
    it_assessment = db.query(Organization).filter(Organization.id == it_assessment_id).first()
    if it_assessment is None:
        raise HTTPException(status_code=404, detail="IT Assessment not found")
    return it_assessment

@router.post("/{client_id}/itAssessment", response_model=ItAssessmentSchema)
async def create_it_assessment(it_assessment: ItAssessmentSchema, db: Session = Depends(get_db)):
    logging.info(f"Creating IT Assessment: {it_assessment}")
    it_assessment = Organization(**it_assessment.dict())
    db.add(it_assessment)
    db.commit
    db.refresh(it_assessment)
    return it_assessment

@router.patch("/{client_id}/itAssessment/{it_assessment_id}", response_model=ItAssessmentSchema)
async def update_it_assessment(it_assessment_id: int, it_assessment: ItAssessmentSchema, db: Session = Depends(get_db)):
    db.query(Organization).filter(Organization.id == it_assessment_id).update(jsonable_encoder(it_assessment))
    db.commit
    return db.query(Organization).filter(Organization.id == it_assessment_id).first()

@router.delete("/{client_id}/itAssessment/{it_assessment_id}")
async def delete_it_assessment(it_assessment_id: int, db: Session = Depends
(get_db)):
    db.query(Organization).filter(Organization.id == it_assessment_id).delete()
    db.commit
    return {"message": "IT Assessment deleted successfully!"}
