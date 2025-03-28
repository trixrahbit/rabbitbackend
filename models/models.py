from sqlalchemy import (
    Column, Integer, String, ForeignKey, Boolean, Table, Date, func, Text, Time, DateTime
)
from sqlalchemy.orm import relationship  # Ensure correct import path
from datetime import datetime
from db_config.db_connection import Base





# ✅ Association table for users and roles (Many-to-Many)
user_roles = Table(
    'user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True)
)

# ✅ Association table for roles and permissions (Many-to-Many)
role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id', ondelete="CASCADE"), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id', ondelete="CASCADE"), primary_key=True)
)




# 🔹 **Organization Model (Owns Subscriptions & Users)**
class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    domain = Column(String, unique=True, nullable=True)
    phone = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    size = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    logo = Column(String, nullable=True)
    website = Column(String, nullable=True)
    revenue = Column(String, nullable=True)
    founded = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    super_admin = Column(Boolean, default=False)

    # ✅ Relationships
    clients = relationship("Client", back_populates="organization", cascade="all, delete-orphan")
    users = relationship("User", back_populates="organization", foreign_keys="[User.organization_id]")
    subscriptions = relationship("Subscription", back_populates="organization", cascade="all, delete-orphan")


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    domain = Column(String, unique=True, nullable=True)
    phone = Column(String, nullable=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)  # ✅ Clients belong to an Org
    type = Column(String, nullable=True)
    industry = Column(String, nullable=True)
    size = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    logo = Column(String, nullable=True)
    website = Column(String, nullable=True)
    revenue = Column(String, nullable=True)
    founded = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # ✅ Relationships
    organization = relationship("Organization", back_populates="clients")
    contacts = relationship("Contact", back_populates="client", cascade="all, delete-orphan")
    tickets = relationship("Ticket", back_populates="client", cascade="all, delete-orphan")
    billing_agreements = relationship("BillingAgreement", back_populates="client", cascade="all, delete-orphan")
    surveys = relationship("Survey", back_populates="client", cascade="all, delete-orphan")
    contracts = relationship("Contract", back_populates="client", cascade="all, delete-orphan")

# 🔹 **User Model (Belongs to Organization, Not Client)**
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    mobile = Column(String)
    location = Column(String)
    hashed_password = Column(String)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)  # ✅ Users belong to an Org
    is_active = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    booking_url = Column(String, unique=True, nullable=True)
    outlook_access_token = Column(String, nullable=True)
    outlook_refresh_token = Column(String, nullable=True)
    outlook_token_expires_at = Column(DateTime, nullable=True)
    time_zone = Column(String, nullable=True)
    agree_to_terms = Column(Boolean, default=False)
    session_timeout = Column(Integer, default=30)  # ✅ New Field (Default: 30 minutes)

    # ✅ Many-to-Many relationship with roles
    roles = relationship('Role', secondary=user_roles, back_populates='users')
    organization = relationship("Organization", back_populates="users", foreign_keys=[organization_id])  # ✅ Fix applied
    business_hours = relationship('BusinessHours', back_populates='user')


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    default = Column(Boolean, default=False)
    super_admin = Column(Boolean, default=False)

    # ✅ Many-to-Many relationships
    users = relationship('User', secondary=user_roles, back_populates='roles')
    permissions = relationship('Permission', secondary=role_permissions, back_populates='roles')


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    # ✅ Relationship to roles
    roles = relationship('Role', secondary=role_permissions, back_populates='permissions')


class ClientRole(Base):
    __tablename__ = 'organization_roles'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))


class BusinessHours(Base):
    __tablename__ = 'business_hours'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), index=True)
    day_of_week = Column(String, index=True)
    start_time = Column(Time)
    end_time = Column(Time)

    # ✅ Relationship
    user = relationship('User', back_populates='business_hours')
