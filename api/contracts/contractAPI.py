import loguru as logging
from fastapi import Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List
from db_config.db_connection import get_db

# Import models
from models.contracts.contractModel import (
    Contract,
    ContractBlock,
    ContractFixedCost,
    ContractMilestone,
    ContractCharge,
    ContractExclusion,
    ExclusionBillingCode,
    ContractRate,
    ContractRoleCost,
    ContractType,
    ContractCategory,
    BillingMilestoneStatus,
    Service, ServiceBundle,
    ContractServiceAssignment,
    ContractServiceBundleAssignment
)

# Import schemas
from schemas.contracts.contractSchema import (
    ContractSchema, ContractCreate, ContractUpdate, ContractFullCreate,
    ContractBlockSchema, ContractBlockCreate,
    ContractFixedCostSchema, ContractFixedCostCreate,
    ContractMilestoneSchema, ContractMilestoneCreate,
    ContractChargeSchema, ContractChargeCreate,
    ContractExclusionSchema, ContractExclusionCreate,
    ExclusionBillingCodeSchema, ExclusionBillingCodeCreate,
    ContractRateSchema, ContractRateCreate,
    ContractRoleCostSchema, ContractRoleCostCreate,
    ContractTypeSchema, ContractTypeCreate,
    ContractCategorySchema, ContractCategoryCreate,
    BillingMilestoneStatusSchema, BillingMilestoneStatusCreate,
    ServiceSchema, ServiceBundleSchema,
    ContractServiceAssignmentSchema, ContractServiceAssignmentCreate,
    ContractServiceBundleAssignmentSchema, ContractServiceBundleAssignmentCreate, ServiceBase, ServiceBundleBase
)

from root.root_elements import router

logger = logging.logger

# --------------------
# Contract Endpoints
# --------------------
@router.get("/contracts", response_model=List[ContractSchema])
async def get_contracts(db: Session = Depends(get_db)):
    contracts = db.query(Contract).all()
    return contracts

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

@router.post("/contracts/full", response_model=ContractSchema)
async def create_full_contract(contract: ContractFullCreate, db: Session = Depends(get_db)):
    try:
        with db.begin():
            contract_data = contract.dict(
                exclude_unset=True,
                exclude={"blocks", "fixed_costs", "milestones", "charges", "exclusions", "rates", "role_costs"}
                # You can choose to exclude service assignments if handled separately.
            )
            db_contract = Contract(**contract_data)
            db.add(db_contract)
            db.flush()
            if contract.blocks:
                for block in contract.blocks:
                    block_data = block.dict()
                    block_data["contract_id"] = db_contract.id
                    db_block = ContractBlock(**block_data)
                    db.add(db_block)
            if contract.fixed_costs:
                for cost in contract.fixed_costs:
                    cost_data = cost.dict()
                    cost_data["contract_id"] = db_contract.id
                    db_cost = ContractFixedCost(**cost_data)
                    db.add(db_cost)
            if contract.milestones:
                for milestone in contract.milestones:
                    milestone_data = milestone.dict()
                    milestone_data["contract_id"] = db_contract.id
                    db_milestone = ContractMilestone(**milestone_data)
                    db.add(db_milestone)
            if contract.charges:
                for charge in contract.charges:
                    charge_data = charge.dict()
                    charge_data["contract_id"] = db_contract.id
                    db_charge = ContractCharge(**charge_data)
                    db.add(db_charge)
            if contract.exclusions:
                for exclusion in contract.exclusions:
                    exclusion_data = exclusion.dict()
                    exclusion_data["contract_id"] = db_contract.id
                    db_exclusion = ContractExclusion(**exclusion_data)
                    db.add(db_exclusion)
                    if exclusion.billing_codes:
                        for code in exclusion.billing_codes:
                            code_data = code.dict()
                            code_data["exclusion_id"] = db_exclusion.id
                            db_code = ExclusionBillingCode(**code_data)
                            db.add(db_code)
            if contract.rates:
                for rate in contract.rates:
                    rate_data = rate.dict()
                    rate_data["contract_id"] = db_contract.id
                    db_rate = ContractRate(**rate_data)
                    db.add(db_rate)
            if contract.role_costs:
                for role_cost in contract.role_costs:
                    role_cost_data = role_cost.dict()
                    role_cost_data["contract_id"] = db_contract.id
                    db_role_cost = ContractRoleCost(**role_cost_data)
                    db.add(db_role_cost)
        db.commit()
        db.refresh(db_contract)
        return db_contract
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --------------------
# Contract Block Endpoints
# --------------------
@router.get("/contracts/{contract_id}/blocks", response_model=List[ContractBlockSchema])
async def get_contract_blocks(contract_id: int, db: Session = Depends(get_db)):
    blocks = db.query(ContractBlock).filter(ContractBlock.contract_id == contract_id).all()
    return blocks

@router.post("/contracts/{contract_id}/blocks", response_model=ContractBlockSchema)
async def create_contract_block(contract_id: int, block: ContractBlockCreate, db: Session = Depends(get_db)):
    if block.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_block = ContractBlock(**block.dict())
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block

@router.put("/contracts/{contract_id}/blocks/{block_id}", response_model=ContractBlockSchema)
async def update_contract_block(contract_id: int, block_id: int, block_data: ContractBlockCreate, db: Session = Depends(get_db)):
    db_block = db.query(ContractBlock).filter(
        ContractBlock.id == block_id,
        ContractBlock.contract_id == contract_id
    ).first()
    if not db_block:
        raise HTTPException(status_code=404, detail="Contract block not found")
    for key, value in block_data.dict(exclude_unset=True).items():
        setattr(db_block, key, value)
    db.commit()
    db.refresh(db_block)
    return db_block

@router.delete("/contracts/{contract_id}/blocks/{block_id}", response_model=ContractBlockSchema)
async def delete_contract_block(contract_id: int, block_id: int, db: Session = Depends(get_db)):
    db_block = db.query(ContractBlock).filter(
        ContractBlock.id == block_id,
        ContractBlock.contract_id == contract_id
    ).first()
    if not db_block:
        raise HTTPException(status_code=404, detail="Contract block not found")
    db.delete(db_block)
    db.commit()
    return db_block

# --------------------
# Contract Fixed Cost Endpoints
# --------------------
@router.get("/contracts/{contract_id}/fixed-costs", response_model=List[ContractFixedCostSchema])
async def get_fixed_costs(contract_id: int, db: Session = Depends(get_db)):
    costs = db.query(ContractFixedCost).filter(ContractFixedCost.contract_id == contract_id).all()
    return costs

@router.post("/contracts/{contract_id}/fixed-costs", response_model=ContractFixedCostSchema)
async def create_fixed_cost(contract_id: int, cost: ContractFixedCostCreate, db: Session = Depends(get_db)):
    if cost.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_cost = ContractFixedCost(**cost.dict())
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost

@router.delete("/contracts/{contract_id}/fixed-costs/{cost_id}", response_model=ContractFixedCostSchema)
async def delete_fixed_cost(contract_id: int, cost_id: int, db: Session = Depends(get_db)):
    cost = db.query(ContractFixedCost).filter(
        ContractFixedCost.id == cost_id,
        ContractFixedCost.contract_id == contract_id
    ).first()
    if not cost:
        raise HTTPException(status_code=404, detail="Fixed cost not found")
    db.delete(cost)
    db.commit()
    return cost

# --------------------
# Contract Milestone Endpoints
# --------------------
@router.get("/contracts/{contract_id}/milestones", response_model=List[ContractMilestoneSchema])
async def get_contract_milestones(contract_id: int, db: Session = Depends(get_db)):
    milestones = db.query(ContractMilestone).filter(ContractMilestone.contract_id == contract_id).all()
    return milestones

@router.post("/contracts/{contract_id}/milestones", response_model=ContractMilestoneSchema)
async def create_contract_milestone(contract_id: int, milestone: ContractMilestoneCreate, db: Session = Depends(get_db)):
    if milestone.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_milestone = ContractMilestone(**milestone.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.put("/contracts/{contract_id}/milestones/{milestone_id}", response_model=ContractMilestoneSchema)
async def update_contract_milestone(contract_id: int, milestone_id: int, milestone_data: ContractMilestoneCreate, db: Session = Depends(get_db)):
    db_milestone = db.query(ContractMilestone).filter(
        ContractMilestone.id == milestone_id,
        ContractMilestone.contract_id == contract_id
    ).first()
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Contract milestone not found")
    for key, value in milestone_data.dict(exclude_unset=True).items():
        setattr(db_milestone, key, value)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.delete("/contracts/{contract_id}/milestones/{milestone_id}", response_model=ContractMilestoneSchema)
async def delete_contract_milestone(contract_id: int, milestone_id: int, db: Session = Depends(get_db)):
    milestone = db.query(ContractMilestone).filter(
        ContractMilestone.id == milestone_id,
        ContractMilestone.contract_id == contract_id
    ).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Contract milestone not found")
    db.delete(milestone)
    db.commit()
    return milestone

# --------------------
# Contract Charge Endpoints
# --------------------
@router.get("/contracts/{contract_id}/charges", response_model=List[ContractChargeSchema])
async def get_contract_charges(contract_id: int, db: Session = Depends(get_db)):
    charges = db.query(ContractCharge).filter(ContractCharge.contract_id == contract_id).all()
    return charges

@router.post("/contracts/{contract_id}/charges", response_model=ContractChargeSchema)
async def create_contract_charge(contract_id: int, charge: ContractChargeCreate, db: Session = Depends(get_db)):
    if charge.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_charge = ContractCharge(**charge.dict())
    db.add(db_charge)
    db.commit()
    db.refresh(db_charge)
    return db_charge

@router.put("/contracts/{contract_id}/charges/{charge_id}", response_model=ContractChargeSchema)
async def update_contract_charge(contract_id: int, charge_id: int, charge_data: ContractChargeCreate, db: Session = Depends(get_db)):
    db_charge = db.query(ContractCharge).filter(
        ContractCharge.id == charge_id,
        ContractCharge.contract_id == contract_id
    ).first()
    if not db_charge:
        raise HTTPException(status_code=404, detail="Contract charge not found")
    for key, value in charge_data.dict(exclude_unset=True).items():
        setattr(db_charge, key, value)
    db.commit()
    db.refresh(db_charge)
    return db_charge

@router.delete("/contracts/{contract_id}/charges/{charge_id}", response_model=ContractChargeSchema)
async def delete_contract_charge(contract_id: int, charge_id: int, db: Session = Depends(get_db)):
    charge = db.query(ContractCharge).filter(
        ContractCharge.id == charge_id,
        ContractCharge.contract_id == contract_id
    ).first()
    if not charge:
        raise HTTPException(status_code=404, detail="Contract charge not found")
    db.delete(charge)
    db.commit()
    return charge

# --------------------
# Contract Exclusion Endpoints
# --------------------
@router.get("/contracts/{contract_id}/exclusions", response_model=List[ContractExclusionSchema])
async def get_contract_exclusions(contract_id: int, db: Session = Depends(get_db)):
    exclusions = db.query(ContractExclusion).filter(ContractExclusion.contract_id == contract_id).all()
    return exclusions

@router.post("/contracts/{contract_id}/exclusions", response_model=ContractExclusionSchema)
async def create_contract_exclusion(contract_id: int, exclusion: ContractExclusionCreate, db: Session = Depends(get_db)):
    if exclusion.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_exclusion = ContractExclusion(**exclusion.dict())
    db.add(db_exclusion)
    db.commit()
    db.refresh(db_exclusion)
    return db_exclusion

@router.put("/contracts/{contract_id}/exclusions/{exclusion_id}", response_model=ContractExclusionSchema)
async def update_contract_exclusion(contract_id: int, exclusion_id: int, exclusion_data: ContractExclusionCreate, db: Session = Depends(get_db)):
    db_exclusion = db.query(ContractExclusion).filter(
        ContractExclusion.id == exclusion_id,
        ContractExclusion.contract_id == contract_id
    ).first()
    if not db_exclusion:
        raise HTTPException(status_code=404, detail="Contract exclusion not found")
    for key, value in exclusion_data.dict(exclude_unset=True).items():
        setattr(db_exclusion, key, value)
    db.commit()
    db.refresh(db_exclusion)
    return db_exclusion

@router.delete("/contracts/{contract_id}/exclusions/{exclusion_id}", response_model=ContractExclusionSchema)
async def delete_contract_exclusion(contract_id: int, exclusion_id: int, db: Session = Depends(get_db)):
    exclusion = db.query(ContractExclusion).filter(
        ContractExclusion.id == exclusion_id,
        ContractExclusion.contract_id == contract_id
    ).first()
    if not exclusion:
        raise HTTPException(status_code=404, detail="Contract exclusion not found")
    db.delete(exclusion)
    db.commit()
    return exclusion

# --------------------
# Exclusion Billing Code Endpoints
# --------------------
@router.get("/exclusions/{exclusion_id}/billing-codes", response_model=List[ExclusionBillingCodeSchema])
async def get_billing_codes(exclusion_id: int, db: Session = Depends(get_db)):
    codes = db.query(ExclusionBillingCode).filter(ExclusionBillingCode.exclusion_id == exclusion_id).all()
    return codes

@router.post("/exclusions/{exclusion_id}/billing-codes", response_model=ExclusionBillingCodeSchema)
async def create_billing_code(exclusion_id: int, code: ExclusionBillingCodeCreate, db: Session = Depends(get_db)):
    if code.exclusion_id != exclusion_id:
        raise HTTPException(status_code=400, detail="Exclusion ID mismatch")
    db_code = ExclusionBillingCode(**code.dict())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code

@router.put("/exclusions/{exclusion_id}/billing-codes/{code_id}", response_model=ExclusionBillingCodeSchema)
async def update_billing_code(exclusion_id: int, code_id: int, code_data: ExclusionBillingCodeCreate, db: Session = Depends(get_db)):
    db_code = db.query(ExclusionBillingCode).filter(
        ExclusionBillingCode.id == code_id,
        ExclusionBillingCode.exclusion_id == exclusion_id
    ).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="Billing code not found")
    for key, value in code_data.dict(exclude_unset=True).items():
        setattr(db_code, key, value)
    db.commit()
    db.refresh(db_code)
    return db_code

@router.delete("/exclusions/{exclusion_id}/billing-codes/{code_id}", response_model=ExclusionBillingCodeSchema)
async def delete_billing_code(exclusion_id: int, code_id: int, db: Session = Depends(get_db)):
    db_code = db.query(ExclusionBillingCode).filter(
        ExclusionBillingCode.id == code_id,
        ExclusionBillingCode.exclusion_id == exclusion_id
    ).first()
    if not db_code:
        raise HTTPException(status_code=404, detail="Billing code not found")
    db.delete(db_code)
    db.commit()
    return db_code

# --------------------
# Contract Rate Endpoints
# --------------------
@router.get("/contracts/{contract_id}/rates", response_model=List[ContractRateSchema])
async def get_contract_rates(contract_id: int, db: Session = Depends(get_db)):
    rates = db.query(ContractRate).filter(ContractRate.contract_id == contract_id).all()
    return rates

@router.post("/contracts/{contract_id}/rates", response_model=ContractRateSchema)
async def create_contract_rate(contract_id: int, rate: ContractRateCreate, db: Session = Depends(get_db)):
    if rate.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_rate = ContractRate(**rate.dict())
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)
    return db_rate

@router.put("/contracts/{contract_id}/rates/{rate_id}", response_model=ContractRateSchema)
async def update_contract_rate(contract_id: int, rate_id: int, rate_data: ContractRateCreate, db: Session = Depends(get_db)):
    db_rate = db.query(ContractRate).filter(
        ContractRate.id == rate_id,
        ContractRate.contract_id == contract_id
    ).first()
    if not db_rate:
        raise HTTPException(status_code=404, detail="Contract rate not found")
    for key, value in rate_data.dict(exclude_unset=True).items():
        setattr(db_rate, key, value)
    db.commit()
    db.refresh(db_rate)
    return db_rate

@router.delete("/contracts/{contract_id}/rates/{rate_id}", response_model=ContractRateSchema)
async def delete_contract_rate(contract_id: int, rate_id: int, db: Session = Depends(get_db)):
    rate = db.query(ContractRate).filter(
        ContractRate.id == rate_id,
        ContractRate.contract_id == contract_id
    ).first()
    if not rate:
        raise HTTPException(status_code=404, detail="Contract rate not found")
    db.delete(rate)
    db.commit()
    return rate

# --------------------
# Contract Role Cost Endpoints
# --------------------
@router.get("/contracts/{contract_id}/role-costs", response_model=List[ContractRoleCostSchema])
async def get_contract_role_costs(contract_id: int, db: Session = Depends(get_db)):
    costs = db.query(ContractRoleCost).filter(ContractRoleCost.contract_id == contract_id).all()
    return costs

@router.post("/contracts/{contract_id}/role-costs", response_model=ContractRoleCostSchema)
async def create_contract_role_cost(contract_id: int, cost: ContractRoleCostCreate, db: Session = Depends(get_db)):
    if cost.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_cost = ContractRoleCost(**cost.dict())
    db.add(db_cost)
    db.commit()
    db.refresh(db_cost)
    return db_cost

@router.put("/contracts/{contract_id}/role-costs/{role_cost_id}", response_model=ContractRoleCostSchema)
async def update_contract_role_cost(contract_id: int, role_cost_id: int, cost_data: ContractRoleCostCreate, db: Session = Depends(get_db)):
    db_cost = db.query(ContractRoleCost).filter(
        ContractRoleCost.id == role_cost_id,
        ContractRoleCost.contract_id == contract_id
    ).first()
    if not db_cost:
        raise HTTPException(status_code=404, detail="Contract role cost not found")
    for key, value in cost_data.dict(exclude_unset=True).items():
        setattr(db_cost, key, value)
    db.commit()
    db.refresh(db_cost)
    return db_cost

@router.delete("/contracts/{contract_id}/role-costs/{role_cost_id}", response_model=ContractRoleCostSchema)
async def delete_contract_role_cost(contract_id: int, role_cost_id: int, db: Session = Depends(get_db)):
    cost = db.query(ContractRoleCost).filter(
        ContractRoleCost.id == role_cost_id,
        ContractRoleCost.contract_id == contract_id
    ).first()
    if not cost:
        raise HTTPException(status_code=404, detail="Contract role cost not found")
    db.delete(cost)
    db.commit()
    return cost

# --------------------
# Contract Service Assignment Endpoints
# --------------------
@router.get("/contracts/{contract_id}/service-assignments", response_model=List[ContractServiceAssignmentSchema])
async def get_contract_service_assignments(contract_id: int, db: Session = Depends(get_db)):
    assignments = db.query(ContractServiceAssignment).filter(ContractServiceAssignment.contract_id == contract_id).all()
    return assignments

@router.post("/contracts/{contract_id}/service-assignments", response_model=ContractServiceAssignmentSchema)
async def create_contract_service_assignment(contract_id: int, assignment: ContractServiceAssignmentCreate, db: Session = Depends(get_db)):
    if assignment.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_assignment = ContractServiceAssignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/contracts/{contract_id}/service-assignments/{assignment_id}", response_model=ContractServiceAssignmentSchema)
async def update_contract_service_assignment(contract_id: int, assignment_id: int, assignment_data: ContractServiceAssignmentCreate, db: Session = Depends(get_db)):
    db_assignment = db.query(ContractServiceAssignment).filter(
        ContractServiceAssignment.id == assignment_id,
        ContractServiceAssignment.contract_id == contract_id
    ).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Contract service assignment not found")
    for key, value in assignment_data.dict(exclude_unset=True).items():
        setattr(db_assignment, key, value)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/contracts/{contract_id}/service-assignments/{assignment_id}", response_model=ContractServiceAssignmentSchema)
async def delete_contract_service_assignment(contract_id: int, assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = db.query(ContractServiceAssignment).filter(
        ContractServiceAssignment.id == assignment_id,
        ContractServiceAssignment.contract_id == contract_id
    ).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Contract service assignment not found")
    db.delete(db_assignment)
    db.commit()
    return db_assignment

# --------------------
# Contract Service Bundle Assignment Endpoints
# --------------------
@router.get("/contracts/{contract_id}/bundle-assignments", response_model=List[ContractServiceBundleAssignmentSchema])
async def get_contract_bundle_assignments(contract_id: int, db: Session = Depends(get_db)):
    assignments = db.query(ContractServiceBundleAssignment).filter(ContractServiceBundleAssignment.contract_id == contract_id).all()
    return assignments

@router.post("/contracts/{contract_id}/bundle-assignments", response_model=ContractServiceBundleAssignmentSchema)
async def create_contract_bundle_assignment(contract_id: int, assignment: ContractServiceBundleAssignmentCreate, db: Session = Depends(get_db)):
    if assignment.contract_id != contract_id:
        raise HTTPException(status_code=400, detail="Contract ID mismatch")
    db_assignment = ContractServiceBundleAssignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/contracts/{contract_id}/bundle-assignments/{assignment_id}", response_model=ContractServiceBundleAssignmentSchema)
async def update_contract_bundle_assignment(contract_id: int, assignment_id: int, assignment_data: ContractServiceBundleAssignmentCreate, db: Session = Depends(get_db)):
    db_assignment = db.query(ContractServiceBundleAssignment).filter(
        ContractServiceBundleAssignment.id == assignment_id,
        ContractServiceBundleAssignment.contract_id == contract_id
    ).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Contract service bundle assignment not found")
    for key, value in assignment_data.dict(exclude_unset=True).items():
        setattr(db_assignment, key, value)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/contracts/{contract_id}/bundle-assignments/{assignment_id}", response_model=ContractServiceBundleAssignmentSchema)
async def delete_contract_bundle_assignment(contract_id: int, assignment_id: int, db: Session = Depends(get_db)):
    db_assignment = db.query(ContractServiceBundleAssignment).filter(
        ContractServiceBundleAssignment.id == assignment_id,
        ContractServiceBundleAssignment.contract_id == contract_id
    ).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Contract service bundle assignment not found")
    db.delete(db_assignment)
    db.commit()
    return db_assignment

# --------------------
# Contract Type Endpoints
# --------------------
@router.get("/contract-types", response_model=List[ContractTypeSchema])
async def get_contract_types(db: Session = Depends(get_db)):
    types = db.query(ContractType).all()
    return types

@router.post("/contract-types", response_model=ContractTypeSchema)
async def create_contract_type(contract_type: ContractTypeCreate, db: Session = Depends(get_db)):
    db_type = ContractType(**contract_type.dict())
    db.add(db_type)
    db.commit()
    db.refresh(db_type)
    return db_type

@router.put("/contract-types/{type_id}", response_model=ContractTypeSchema)
async def update_contract_type(type_id: int, contract_type: ContractTypeCreate, db: Session = Depends(get_db)):
    db_type = db.query(ContractType).filter(ContractType.id == type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Contract type not found")
    for key, value in contract_type.dict(exclude_unset=True).items():
        setattr(db_type, key, value)
    db.commit()
    db.refresh(db_type)
    return db_type

@router.delete("/contract-types/{type_id}", response_model=ContractTypeSchema)
async def delete_contract_type(type_id: int, db: Session = Depends(get_db)):
    db_type = db.query(ContractType).filter(ContractType.id == type_id).first()
    if not db_type:
        raise HTTPException(status_code=404, detail="Contract type not found")
    db.delete(db_type)
    db.commit()
    return db_type

# --------------------
# Contract Category Endpoints
# --------------------
@router.get("/contract-categories", response_model=List[ContractCategorySchema])
async def get_contract_categories(db: Session = Depends(get_db)):
    categories = db.query(ContractCategory).all()
    return categories

@router.post("/contract-categories", response_model=ContractCategorySchema)
async def create_contract_category(category: ContractCategoryCreate, db: Session = Depends(get_db)):
    db_category = ContractCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/contract-categories/{category_id}", response_model=ContractCategorySchema)
async def update_contract_category(category_id: int, category_data: ContractCategoryCreate, db: Session = Depends(get_db)):
    db_category = db.query(ContractCategory).filter(ContractCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Contract category not found")
    for key, value in category_data.dict(exclude_unset=True).items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/contract-categories/{category_id}", response_model=ContractCategorySchema)
async def delete_contract_category(category_id: int, db: Session = Depends(get_db)):
    db_category = db.query(ContractCategory).filter(ContractCategory.id == category_id).first()
    if not db_category:
        raise HTTPException(status_code=404, detail="Contract category not found")
    db.delete(db_category)
    db.commit()
    return db_category

# --------------------
# Billing Milestone Status Endpoints
# --------------------
@router.get("/billing-milestone-statuses", response_model=List[BillingMilestoneStatusSchema])
async def get_billing_milestone_statuses(db: Session = Depends(get_db)):
    statuses = db.query(BillingMilestoneStatus).all()
    return statuses

@router.post("/billing-milestone-statuses", response_model=BillingMilestoneStatusSchema)
async def create_billing_milestone_status(status: BillingMilestoneStatusCreate, db: Session = Depends(get_db)):
    db_status = BillingMilestoneStatus(**status.dict())
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status

@router.put("/billing-milestone-statuses/{status_id}", response_model=BillingMilestoneStatusSchema)
async def update_billing_milestone_status(status_id: int, status_data: BillingMilestoneStatusCreate, db: Session = Depends(get_db)):
    db_status = db.query(BillingMilestoneStatus).filter(BillingMilestoneStatus.id == status_id).first()
    if not db_status:
        raise HTTPException(status_code=404, detail="Billing milestone status not found")
    for key, value in status_data.dict(exclude_unset=True).items():
        setattr(db_status, key, value)
    db.commit()
    db.refresh(db_status)
    return db_status

@router.delete("/billing-milestone-statuses/{status_id}", response_model=BillingMilestoneStatusSchema)
async def delete_billing_milestone_status(status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(BillingMilestoneStatus).filter(BillingMilestoneStatus.id == status_id).first()
    if not db_status:
        raise HTTPException(status_code=404, detail="Billing milestone status not found")
    db.delete(db_status)
    db.commit()
    return db_status



@router.get("/services", response_model=List[ServiceSchema])
async def get_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    return services

@router.post("/services", response_model=ServiceSchema)
async def create_service(service: ServiceBase, db: Session = Depends(get_db)):
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


@router.put("/services/{service_id}", response_model=ServiceSchema)
async def update_service(service_id: int, service_data: ServiceSchema, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    for key, value in service_data.dict(exclude_unset=True).items():
        setattr(db_service, key, value)
    db.commit()
    db.refresh(db_service)
    return db_service

@router.delete("/services/{service_id}", response_model=ServiceSchema)
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    db_service = db.query(Service).filter(Service.id == service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")
    db.delete(db_service)
    db.commit()
    return db_service


@router.get("/service-bundles", response_model=List[ServiceBundleSchema])
async def get_service_bundles(db: Session = Depends(get_db)):
    bundles = db.query(ServiceBundle).all()
    return bundles


@router.post("/service-bundles", response_model=ServiceBundleSchema)
async def create_service_bundle(bundle: ServiceBundleCreate, db: Session = Depends(get_db)):
    # Create the ServiceBundle object without services first.
    db_bundle = ServiceBundle(
        bundle_name=bundle.bundle_name,
        price=bundle.price,
        cost=bundle.cost
    )
    db.add(db_bundle)
    db.commit()
    db.refresh(db_bundle)

    # If there are service IDs provided, associate them.
    if bundle.service_ids:
        # Query the Service objects by their IDs.
        services = db.query(Service).filter(Service.id.in_(bundle.service_ids)).all()
        db_bundle.services = services
        db.commit()
        db.refresh(db_bundle)

    return db_bundle


@router.put("/service-bundles/{bundle_id}", response_model=ServiceBundleSchema)
async def update_service_bundle(bundle_id: int, bundle_data: ServiceBundleBase, db: Session = Depends(get_db)):
    db_bundle = db.query(ServiceBundle).filter(ServiceBundle.id == bundle_id).first()
    if not db_bundle:
        raise HTTPException(status_code=404, detail="Service bundle not found")
    for key, value in bundle_data.dict(exclude_unset=True).items():
        setattr(db_bundle, key, value)
    db.commit()
    db.refresh(db_bundle)
    return db_bundle


@router.delete("/service-bundles/{bundle_id}", response_model=ServiceBundleSchema)
async def delete_service_bundle(bundle_id: int, db: Session = Depends(get_db)):
    db_bundle = db.query(ServiceBundle).filter(ServiceBundle.id == bundle_id).first()
    if not db_bundle:
        raise HTTPException(status_code=404, detail="Service bundle not found")
    db.delete(db_bundle)
    db.commit()
    return db_bundle


