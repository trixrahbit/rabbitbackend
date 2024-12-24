from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table, DateTime, func, Float, Date, Text, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from models import Base

# Association table for users and roles
user_roles = Table('user_role', Base.metadata,
                   Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
                   Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True))

# Association table for roles and permissions
role_permissions = Table('role_permissions', Base.metadata,
                         Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
                         Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True))


class Client(Base):
    __tablename__ = 'clients'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    domain = Column(String, unique=True)
    phone = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))
    type = Column(String)  # e.g., Business, Non-profit, Government
    industry = Column(String)
    size = Column(String)  # e.g., Small, Medium, Large
    description = Column(String)
    logo = Column(String)
    website = Column(String)
    revenue = Column(String)
    founded = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    organizations = relationship('Organization', back_populates='client')
    users = relationship('User', back_populates='client', foreign_keys='User.client_id')


class Organization(Base):
    __tablename__ = 'organizations'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    domain = Column(String, unique=True)
    phone = Column(String)
    creator_id = Column(Integer, ForeignKey('users.id'))
    client_id = Column(Integer, ForeignKey('clients.id'))
    type = Column(String)  # e.g., Business, Non-profit, Government
    industry = Column(String)
    size = Column(String)  # e.g., Small, Medium, Large
    description = Column(String)
    logo = Column(String)
    website = Column(String)
    revenue = Column(String)
    founded = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    client = relationship('Client', back_populates='organizations')
    users = relationship('User', back_populates='organizations', foreign_keys='User.organization_id')
    contacts = relationship('Contact', back_populates='organization')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    mobile = Column(String)
    location = Column(String)
    hashed_password = Column(String)
    client_id = Column(Integer, ForeignKey('clients.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    booking_url = Column(String, unique=True, nullable=True)
    outlook_access_token = Column(String, nullable=True)
    outlook_refresh_token = Column(String, nullable=True)
    outlook_token_expires_at = Column(DateTime, nullable=True)
    time_zone = Column(String, nullable=True)

    # Many-to-Many relationship with roles through user_roles
    roles = relationship('Role', secondary=user_roles, back_populates='users')

    # Relationships
    client = relationship('Client', back_populates='users', foreign_keys=[client_id])
    organizations = relationship('Organization', back_populates='users', foreign_keys=[organization_id])
    business_hours = relationship('BusinessHours', back_populates='user')


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    default = Column(Boolean, default=False)
    super_admin = Column(Boolean, default=False)

    # Relationship back to users
    users = relationship('User', secondary=user_roles, back_populates='roles')


class ClientRole(Base):
    __tablename__ = 'organization_roles'
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('clients.id'))
    role_id = Column(Integer, ForeignKey('roles.id'))


class Contact(Base):
    __tablename__ = 'contacts'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship('Organization', back_populates='contacts')


class BusinessHours(Base):
    __tablename__ = 'business_hours'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), index=True)  # Add ForeignKey here
    day_of_week = Column(String, index=True)
    start_time = Column(Time)
    end_time = Column(Time)

    # Relationships
    user = relationship('User', back_populates='business_hours')



