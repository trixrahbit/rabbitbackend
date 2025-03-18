from typing import Optional, List
from pydantic import BaseModel


# ------------------------
# Contract Schemas
# ------------------------

class ContractBase(BaseModel):
    client_id: int
    pricing: Optional[float] = None
    details: Optional[str] = None
    start_date: str  # ISO date format, e.g. "2025-04-01"
    end_date: Optional[str] = None


class ContractCreate(ContractBase):
    pass


class ContractSchema(ContractBase):
    id: int
    blocks: Optional[List["ContractBlockSchema"]] = []
    milestones: Optional[List["ContractMilestoneSchema"]] = []
    charges: Optional[List["ContractChargeSchema"]] = []
    exclusions: Optional[List["ContractExclusionSchema"]] = []
    rates: Optional[List["ContractRateSchema"]] = []
    role_costs: Optional[List["ContractRoleCostSchema"]] = []

    # Note: services and service_bundles are now represented via assignments in separate endpoints.
    class Config:
        orm_mode = True


class ContractUpdate(ContractBase):
    pass


class ContractFullCreate(ContractCreate):
    blocks: Optional[List["ContractBlockCreate"]] = []
    fixed_costs: Optional[List["ContractFixedCostCreate"]] = []
    milestones: Optional[List["ContractMilestoneCreate"]] = []
    charges: Optional[List["ContractChargeCreate"]] = []
    exclusions: Optional[List["ContractExclusionCreate"]] = []
    rates: Optional[List["ContractRateCreate"]] = []
    role_costs: Optional[List["ContractRoleCostCreate"]] = []
    # If needed, you could also include service or bundle assignments here.


# ------------------------
# Contract Block Schemas
# ------------------------

class ContractBlockBase(BaseModel):
    name: str
    description: Optional[str] = None


class ContractBlockCreate(ContractBlockBase):
    contract_id: int


class ContractBlockSchema(ContractBlockBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Fixed Cost Schemas
# ------------------------

class ContractFixedCostBase(BaseModel):
    amount: float
    description: Optional[str] = None


class ContractFixedCostCreate(ContractFixedCostBase):
    contract_id: int


class ContractFixedCostSchema(ContractFixedCostBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Milestone Schemas
# ------------------------

class ContractMilestoneBase(BaseModel):
    milestone_name: str
    due_date: Optional[str] = None


class ContractMilestoneCreate(ContractMilestoneBase):
    contract_id: int


class ContractMilestoneSchema(ContractMilestoneBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Charge Schemas
# ------------------------

class ContractChargeBase(BaseModel):
    amount: float
    description: Optional[str] = None


class ContractChargeCreate(ContractChargeBase):
    contract_id: int


class ContractChargeSchema(ContractChargeBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Exclusion Schemas
# ------------------------

class ContractExclusionBase(BaseModel):
    description: Optional[str] = None


class ContractExclusionCreate(ContractExclusionBase):
    contract_id: int


class ContractExclusionSchema(ContractExclusionBase):
    id: int
    contract_id: int
    billing_codes: Optional[List["ExclusionBillingCodeSchema"]] = []

    class Config:
        orm_mode = True


# ------------------------
# Exclusion Billing Code Schemas
# ------------------------

class ExclusionBillingCodeBase(BaseModel):
    code: str
    description: Optional[str] = None


class ExclusionBillingCodeCreate(ExclusionBillingCodeBase):
    exclusion_id: int


class ExclusionBillingCodeSchema(ExclusionBillingCodeBase):
    id: int
    exclusion_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Rate Schemas
# ------------------------

class ContractRateBase(BaseModel):
    rate: float
    description: Optional[str] = None


class ContractRateCreate(ContractRateBase):
    contract_id: int


class ContractRateSchema(ContractRateBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Role Cost Schemas
# ------------------------

class ContractRoleCostBase(BaseModel):
    role: str
    cost: float


class ContractRoleCostCreate(ContractRoleCostBase):
    contract_id: int


class ContractRoleCostSchema(ContractRoleCostBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Global Service and Bundle Schemas
# ------------------------

class ServiceBase(BaseModel):
    service_name: str
    price: float
    cost: float


class ServiceSchema(ServiceBase):
    id: int

    class Config:
        orm_mode = True


class ServiceBundleBase(BaseModel):
    bundle_name: str
    price: float
    cost: float

class ServiceBundleCreate(ServiceBundleBase):
    service_ids: Optional[List[int]] = []  # List of service IDs to attach


class ServiceBundleSchema(ServiceBundleBase):
    id: int
    services: Optional[List["ServiceSchema"]] = []

    class Config:
        orm_mode = True


# ------------------------
# Contract Service Assignment Schemas
# ------------------------

class ContractServiceAssignmentBase(BaseModel):
    service_id: int
    price: Optional[float] = None
    cost: Optional[float] = None
    units: Optional[int] = None


class ContractServiceAssignmentCreate(ContractServiceAssignmentBase):
    contract_id: int


class ContractServiceAssignmentSchema(ContractServiceAssignmentBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Service Bundle Assignment Schemas
# ------------------------

class ContractServiceBundleAssignmentBase(BaseModel):
    bundle_id: int
    units: Optional[int] = None


class ContractServiceBundleAssignmentCreate(ContractServiceBundleAssignmentBase):
    contract_id: int


class ContractServiceBundleAssignmentSchema(ContractServiceBundleAssignmentBase):
    id: int
    contract_id: int

    class Config:
        orm_mode = True


# ------------------------
# Contract Type, Category, Billing Milestone Status Schemas
# ------------------------

class ContractTypeBase(BaseModel):
    name: str


class ContractTypeCreate(ContractTypeBase):
    pass


class ContractTypeSchema(ContractTypeBase):
    id: int

    class Config:
        orm_mode = True


class ContractCategoryBase(BaseModel):
    name: str


class ContractCategoryCreate(ContractCategoryBase):
    pass


class ContractCategorySchema(ContractCategoryBase):
    id: int

    class Config:
        orm_mode = True


class BillingMilestoneStatusBase(BaseModel):
    name: str


class BillingMilestoneStatusCreate(BillingMilestoneStatusBase):
    pass


class BillingMilestoneStatusSchema(BillingMilestoneStatusBase):
    id: int

    class Config:
        orm_mode = True


# For forward references
ContractSchema.update_forward_refs()
ContractBlockSchema.update_forward_refs()
ContractFixedCostSchema.update_forward_refs()
ContractMilestoneSchema.update_forward_refs()
ContractChargeSchema.update_forward_refs()
ContractExclusionSchema.update_forward_refs()
ExclusionBillingCodeSchema.update_forward_refs()
ContractRateSchema.update_forward_refs()
ContractRoleCostSchema.update_forward_refs()
ServiceSchema.update_forward_refs()
ServiceBundleSchema.update_forward_refs()
ContractServiceAssignmentSchema.update_forward_refs()
ContractServiceBundleAssignmentSchema.update_forward_refs()
