from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db_config.db_connection import Base

class Asset(Base):
    __tablename__ = 'assets'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    type_id = Column(Integer, ForeignKey('asset_types.id'))
    organization_id = Column(Integer, ForeignKey('organizations.id'))
    status = Column(String)  # Active, In Maintenance, Decommissioned, etc.
    project_id = Column(Integer, ForeignKey('projects.id'))
    billing_agreement_id = Column(Integer, ForeignKey('billing_agreements.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    creator_id = Column(Integer, ForeignKey('users.id'))
    last_updated_by_id = Column(Integer, ForeignKey('users.id'))


    # Relationships
    organization = relationship("Organization", back_populates="assets")
    project = relationship("Project", back_populates="assets")
    billing_agreement = relationship("BillingAgreement", back_populates="assets")
    tickets = relationship("Ticket", back_populates="assets")
    creator = relationship("User", foreign_keys=[creator_id])
    last_updated_by = relationship("User", foreign_keys=[last_updated_by_id])
    type = relationship("AssetTypeModel", back_populates="assets")
    billing_agreement_item = relationship("BillingAgreementItem", back_populates="asset")


class AssetTypeModel(Base):
    __tablename__ = 'asset_types'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    creator_id = Column(Integer, ForeignKey('users.id'))
    last_updated_by_id = Column(Integer, ForeignKey('users.id'))

    # Relationships
    creator = relationship("User", foreign_keys=[creator_id])
    last_updated_by = relationship("User", foreign_keys=[last_updated_by_id])
    assets = relationship("Asset", back_populates="type")

