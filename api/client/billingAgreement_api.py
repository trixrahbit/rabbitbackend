from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from db_config.db_connection import get_db
from models.models import Organization
from schemas.client.billingAgreement_schema import BillingAgreementSchema

router = APIRouter()


@router.get("/{client_id}/{org_id}/billingAgreement", response_model=List[BillingAgreementSchema])
async def get_billing_agreement(client_id: int, org_id: int, db: Session = Depends(get_db)):
    billing_agreement = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if billing_agreement is None:
        raise HTTPException(status_code=404, detail="Billing Agreement not found")
    return billing_agreement.billing_agreement


@router.get("/{client_id}/{org_id}/billingAgreement/{billing_agreement_id}", response_model=BillingAgreementSchema)
async def get_billing_agreement_by_id(client_id: int, org_id: int, billing_agreement_id: int, db: Session = Depends(get_db)):
    billing_agreement = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if billing_agreement is None:
        raise HTTPException(status_code=404, detail="Billing Agreement not found")
    return billing_agreement.billing_agreement[billing_agreement_id]

@router.get("/{client_id}/billingAgreement/", response_model=List[BillingAgreementSchema])
async def get_all_billing_agreements(client_id: int, db: Session = Depends(get_db)):
    billing_agreement = db.query(Organization).filter(Organization.client_id == client_id).all()
    if billing_agreement is None:
        raise HTTPException(status_code=404, detail="Billing Agreement not found")
    return billing_agreement.billing_agreement

@router.post("/{client_id}/{org_id}/billingAgreement", response_model=BillingAgreementSchema)
async def create_billing_agreement(client_id: int, org_id: int, billing_agreement: BillingAgreementSchema, db: Session = Depends(get_db)):
    billing_agreement = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if billing_agreement is None:
        raise HTTPException(status_code=404, detail="Billing Agreement not found")
    billing_agreement.billing_agreement.append(billing_agreement)
    db.commit()
    db.refresh(billing_agreement)
    return billing_agreement

@router.patch("/{client_id}/{org_id}/billingAgreement/{billing_agreement_id}", response_model=BillingAgreementSchema)
async def update_billing_agreement(client_id: int, org_id: int, billing_agreement_id: int, billing_agreement: BillingAgreementSchema, db: Session = Depends(get_db)):
    billing_agreement = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if billing_agreement is None:
        raise HTTPException(status_code=404, detail="Billing Agreement not found")
    billing_agreement.billing_agreement[billing_agreement_id] = billing_agreement
    db.commit()
    db.refresh(billing_agreement)
    return billing_agreement

@router.delete("/{client_id}/{org_id}/billingAgreement/{billing_agreement_id}", response_model=BillingAgreementSchema)
async def delete_billing_agreement(client_id: int, org_id: int, billing_agreement_id: int, db: Session = Depends(get_db)):
    billing_agreement = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if billing_agreement is None:
        raise HTTPException(status_code=404, detail="Billing Agreement not found")
    billing_agreement.billing_agreement.pop(billing_agreement_id)
    db.commit()
    db.refresh(billing_agreement)
    return billing_agreement