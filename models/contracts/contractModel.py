from sqlalchemy import Column, Integer, String, Text, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from db_config.db_connection import Base

# ------------------------
# Contract Model and Related Tables
# ------------------------

class Contract(Base):
    __tablename__ = 'contracts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    pricing = Column(Float, nullable=True)
    details = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)

    # Relationships for other contract details:
    blocks = relationship("ContractBlock", back_populates="contract", cascade="all, delete-orphan")
    milestones = relationship("ContractMilestone", back_populates="contract", cascade="all, delete-orphan")
    charges = relationship("ContractCharge", back_populates="contract", cascade="all, delete-orphan")
    exclusions = relationship("ContractExclusion", back_populates="contract", cascade="all, delete-orphan")
    rates = relationship("ContractRate", back_populates="contract", cascade="all, delete-orphan")
    role_costs = relationship("ContractRoleCost", back_populates="contract", cascade="all, delete-orphan")
    fixed_costs = relationship("ContractFixedCost", back_populates="contract", cascade="all, delete-orphan")

    # Linking tables for global services and bundles:
    service_assignments = relationship("ContractServiceAssignment", back_populates="contract", cascade="all, delete-orphan")
    bundle_assignments = relationship("ContractServiceBundleAssignment", back_populates="contract", cascade="all, delete-orphan")

    client = relationship("Client", back_populates="contracts")
    tickets = relationship("Ticket", back_populates="contracts")


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


# ------------------------
# Global Service and Bundle Models
# ------------------------

class Service(Base):
    __tablename__ = 'contract_services'  # Updated table name to "services"
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)


class ServiceBundle(Base):
    __tablename__ = 'contract_service_bundles'  # Updated table name to "service_bundles"
    id = Column(Integer, primary_key=True, autoincrement=True)
    bundle_name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    cost = Column(Float, nullable=False)
    # Additional fields can be added as needed.


# ------------------------
# Linking Tables for Contract-Service and Contract-Bundle Assignments
# ------------------------

class ContractServiceAssignment(Base):
    __tablename__ = 'contract_service_assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    # Contract-specific overrides
    price = Column(Float, nullable=True)
    cost = Column(Float, nullable=True)
    units = Column(Integer, nullable=True)

    contract = relationship("Contract", back_populates="service_assignments")
    service = relationship("Service")


class ContractServiceBundleAssignment(Base):
    __tablename__ = 'contract_service_bundle_assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    contract_id = Column(Integer, ForeignKey('contracts.id'), nullable=False)
    bundle_id = Column(Integer, ForeignKey('service_bundles.id'), nullable=False)
    units = Column(Integer, nullable=True)

    contract = relationship("Contract", back_populates="bundle_assignments")
    bundle = relationship("ServiceBundle")


# ------------------------
# Additional Contract Lookup Tables
# ------------------------

class ContractType(Base):
    __tablename__ = 'contract_types'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class ContractCategory(Base):
    __tablename__ = 'contract_categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)


class BillingMilestoneStatus(Base):
    __tablename__ = 'billing_milestone_statuses'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
