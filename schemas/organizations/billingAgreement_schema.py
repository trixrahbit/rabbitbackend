from typing import Optional, List

from pydantic import BaseModel, constr, EmailStr

class BillingAgreementSchema(BaseModel):
    name: str
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    organization_id: Optional[int] = None
    status: str
    sla_condition_id: Optional[int] = None


    class Config:
        from_attributes = True


class BillingAgreementUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    organization_id: Optional[int] = None
    status: Optional[str] = None
    sla_condition_id: Optional[int] = None

    class Config:
        from_attributes = True

class BillingAgreementResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    organization_id: Optional[int] = None
    status: str
    sla_condition_id: Optional[int] = None

    class Config:
        from_attributes = True


class BillingAgreementListResponseSchema(BaseModel):
    billing_agreements: List[BillingAgreementResponseSchema]

    class Config:
        from_attributes = True

class BillingAgreementItemSchema(BaseModel):
    name: str
    description: str
    quantity: int
    price: float
    billing_agreement_id: Optional[int] = None
    status: str

    class Config:
        from_attributes = True

class BillingAgreementItemUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    quantity: Optional[int] = None
    price: Optional[float] = None
    billing_agreement_id: Optional[int] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

class BillingAgreementItemResponseSchema(BaseModel):
    id: int
    name: str
    description: str
    quantity: int
    price: float
    billing_agreement_id: Optional[int] = None
    status: str

    class Config:
        from_attributes = True

class BillingAgreementItemListResponseSchema(BaseModel):
    billing_agreement_items: List[BillingAgreementItemResponseSchema]

    class Config:
        from_attributes = True



