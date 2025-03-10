from fastapi import APIRouter


# @router.get("/{client_id}/leads", response_model=List[Lead])
# def get_leads(client_id: int, db: Session = Depends(get_db)):
#     leads = db.query(Lead).filter(Lead.client_id == client_id).all()
#     return leads
#
# @router.get("/{client_id}/leads/{lead_id}", response_model=Lead)
# def get_lead(client_id: int, lead_id: int, db: Session = Depends(get_db)):
#     lead = db.query(Lead).filter(Lead.id == lead_id, Lead.client_id == client_id).first()
#     if lead is None:
#         raise HTTPException(status_code=404, detail="Lead not found")
#     return lead
#
# @router.post("/{client_id}/leads", response_model=Lead)
# def create_lead(client_id: int, lead: Lead, db: Session = Depends(get_db)):
#     lead.client_id = client_id
#     db.add(lead)
#     db.commit()
#     db.refresh(lead)
#     return lead
#
# @router.put("/{client_id}/leads/{lead_id}", response_model=Lead)
# def update_lead(client_id: int, lead_id: int, lead: Lead, db: Session = Depends(get_db)):
#     db_lead = db.query(Lead).filter(Lead.id == lead_id, Lead.client_id == client_id).first()
#     if db_lead is None:
#         raise HTTPException(status_code=404, detail="Lead not found")
#     update_data = lead.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_lead, key, value)
#     db.commit()
#     db.refresh(db_lead)
#     return db_lead
#
# @router.delete("/{client_id}/leads/{lead_id}", response_model=Lead)
# def delete_lead(client_id: int, lead_id: int, db: Session = Depends(get_db)):
#     db_lead = db.query(Lead).filter(Lead.id == lead_id, Lead.client_id == client_id).first()
#     if db_lead is None:
#         raise HTTPException(status_code=404, detail="Lead not found")
#     db.delete(db_lead)
#     db.commit()
#     return db_lead


