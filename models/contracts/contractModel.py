from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_config.db_connection import Base


class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    pricing = Column(Float, nullable=True)
    details = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Relationships
    blocks = relationship("ContractBlock", back_populates="contract", cascade="all, delete-orphan")
    milestones = relationship("ContractMilestone", back_populates="contract", cascade="all, delete-orphan")
    charges = relationship("ContractCharge", back_populates="contract", cascade="all, delete-orphan")
    exclusions = relationship("ContractExclusion", back_populates="contract", cascade="all, delete-orphan")
    rates = relationship("ContractRate", back_populates="contract", cascade="all, delete-orphan")
    role_costs = relationship("ContractRoleCost", back_populates="contract", cascade="all, delete-orphan")
    client = relationship("Client", back_populates="contracts")
    tickets = relationship("Ticket", back_populates="contracts")
    services = relationship("ContractService", back_populates="contract", cascade="all, delete-orphan")
    service_bundles = relationship("ContractServiceBundle", back_populates="contract", cascade="all, delete-orphan")


class ContractBlock(Base):
    __tablename__ = 'contract_blocks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    contract = relationship("Contract", back_populates="blocks")

class ContractFixedCost(Base):
    __tablename__ = 'contract_fixed_charges'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    contract = relationship("Contract", back_populates="fixed_costs")


class ContractMilestone(Base):
    __tablename__ = 'contract_milestones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    milestone_name = Column(String(255), nullable=False)
    due_date = Column(Date, nullable=True)

    contract = relationship("Contract", back_populates="milestones")


class ContractCharge(Base):
    __tablename__ = 'contract_charges'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    contract = relationship("Contract", back_populates="charges")


class ContractExclusion(Base):
    __tablename__ = 'contract_exclusions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    description = Column(Text, nullable=True)

    contract = relationship("Contract", back_populates="exclusions")
    billing_codes = relationship("ExclusionBillingCode", back_populates="exclusion", cascade="all, delete-orphan")


class ExclusionBillingCode(Base):
    __tablename__ = 'exclusion_billing_codes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    exclusion_id = Column(Integer, ForeignKey('contract_exclusions.id'), nullable=False)
    code = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    exclusion = relationship("ContractExclusion", back_populates="billing_codes")


class ContractRate(Base):
    __tablename__ = 'contract_rates'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    rate = Column(Float, nullable=False)
    description = Column(Text, nullable=True)

    contract = relationship("Contract", back_populates="rates")


class ContractRoleCost(Base):
    __tablename__ = 'contract_role_costs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    role = Column(String(255), nullable=False)
    cost = Column(Float, nullable=False)

    contract = relationship("Contract", back_populates="role_costs")


class ContractService(Base):
    __tablename__ = 'contract_services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    service_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    contract = relationship("Contract", back_populates="services")


class ContractServiceBundle(Base):
    __tablename__ = 'contract_service_bundles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    bundle_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    contract = relationship("Contract", back_populates="service_bundles")
    units = relationship("ContractServiceBundleUnit", back_populates="bundle", cascade="all, delete-orphan")


class ContractServiceBundleUnit(Base):
    __tablename__ = 'contract_service_bundle_units'

    id = Column(Integer, primary_key=True, autoincrement=True)
    bundle_id = Column(Integer, ForeignKey('contract_service_bundles.id'), nullable=False)
    unit_count = Column(Integer, nullable=False)

    bundle = relationship("ContractServiceBundle", back_populates="units")