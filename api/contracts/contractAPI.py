import loguru as logging
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db_config.db_connection import get_db
from models.contracts.contractModel import Contract
from root.root_elements import router  # Assuming you're using a shared router instance
from schemas.contracts.contractSchema import ContractSchema, ContractCreate, ContractUpdate


@router.get("/contracts", response_model=List[ContractSchema])
async def get_contracts(db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    return contracts

@router.get("/contracts/{contract_id}", response_model=ContractSchema)
async def get_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@router.post("/contracts", response_model=ContractSchema)
async def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    db_contract = Contract(**contract.dict())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router.put("/contracts/{contract_id}", response_model=ContractSchema)
async def update_contract(contract_id: int, contract_data: ContractUpdate, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    for key, value in contract_data.dict(exclude_unset=True).items():
        setattr(db_contract, key, value)
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router.delete("/contracts/{contract_id}", response_model=ContractSchema)
async def delete_contract(contract_id: int, db: Session = Depends(get_db)):
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    db.delete(contract)
    db.commit()
    return contract
