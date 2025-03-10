from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.orm import Session
from api.user.user_router import get_db
from models.models import Organization
from root.root_elements import router
from schemas.organizations.accountReview_schema import AccountReviewSchema



@router.get("/{client_id}/{org_id}/accountReview", response_model=List[AccountReviewSchema])
async def get_account_review(client_id: int, org_id: int, db: Session = Depends(get_db)):
    account_review = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if account_review is None:
        raise HTTPException(status_code=404, detail="Account Review not found")
    return account_review.account_review

@router.get("/{client_id}/accountReview", response_model=List[AccountReviewSchema])
async def get_account_review(client_id: int, db: Session = Depends(get_db)):
    account_review = db.query(Organization).filter(Organization.client_id == client_id).first()
    if account_review is None:
        raise HTTPException(status_code=404, detail="Account Review not found")
    return account_review.account_review

@router.get("/{client_id}/{org_id}/accountReview/{account_review_id}", response_model=AccountReviewSchema)
async def get_account_review(client_id: int, org_id: int, account_review_id: int, db: Session = Depends(get_db)):
    account_review = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if account_review is None:
        raise HTTPException(status_code=404, detail="Account Review not found")
    return account_review.account_review[account_review_id]




@router.patch("/{client_id}/{org_id}/accountReview/{account_review_id}/", response_model=AccountReviewSchema)
async def update_account_review(client_id: int, org_id: int, account_review_id: int, account_review: AccountReviewSchema, db: Session = Depends(get_db)):
    account_review = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if account_review is None:
        raise HTTPException(status_code=404, detail="Account Review not found")
    account_review.account_review[account_review_id] = account_review
    db.commit()
    db.refresh(account_review)
    return account_review



@router.post("/{client_id}/{org_id}/accountReview", response_model=AccountReviewSchema)
async def create_account_review(client_id: int, org_id: int, account_review: AccountReviewSchema, db: Session = Depends(get_db)):
    account_review = Organization(client_id=client_id, org_id=org_id, account_review=account_review)
    db.add(account_review)
    db.commit()
    db.refresh(account_review)
    return account_review


@router.delete("/{client_id}/{org_id}/accountReview/{account_review_id}", response_model=AccountReviewSchema)
async def delete_account_review(client_id: int, org_id: int, db: Session = Depends(get_db)):
    account_review = db.query(Organization).filter(Organization.client_id == client_id, Organization.org_id == org_id).first()
    if account_review is None:
        raise HTTPException(status_code=404, detail="Account Review not found")
    db.delete(account_review)
    db.commit()
    return account_review


