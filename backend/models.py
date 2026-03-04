from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, Table, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import date

# Association table for parent-camper relationship
parent_camper_association = Table(
    'parent_camper',
    Base.metadata,
    Column('parent_id', Integer, ForeignKey('parents.id')),
    Column('camper_id', Integer, ForeignKey('campers.id'))
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=False)  # "admin", "parent", "worker"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    parent_profile = relationship("Parent", back_populates="user", uselist=False)
    worker_profile = relationship("CampWorker", back_populates="user", uselist=False)

class Parent(Base):
    __tablename__ = "parents"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    phone = Column(String)
    address = Column(String)
    emergency_contact = Column(String)
    emergency_phone = Column(String)
    
    # Relationships
    user = relationship("User", back_populates="parent_profile")
    campers = relationship("Camper", secondary=parent_camper_association, back_populates="parents")

class CampWorker(Base):
    __tablename__ = "camp_workers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    position = Column(String)  # "counselor", "manager", "support"
    hire_date = Column(Date, default=date.today)
    
    # Relationships
    user = relationship("User", back_populates="worker_profile")

class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    age_min = Column(Integer)
    age_max = Column(Integer)
    max_capacity = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    campers = relationship("Camper", back_populates="group")

class Camper(Base):
    __tablename__ = "campers"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String)
    age = Column(Integer)
    group_id = Column(Integer, ForeignKey("groups.id"))
    is_active = Column(Boolean, default=True)
    is_suspended = Column(Boolean, default=False)
    enrollment_date = Column(Date, default=date.today)
    notes = Column(Text)
    
    # Relationships
    group = relationship("Group", back_populates="campers")
    parents = relationship("Parent", secondary=parent_camper_association, back_populates="campers")
    medical_info = relationship("MedicalInfo", back_populates="camper", uselist=False)
    emergency_contacts = relationship("EmergencyContact", back_populates="camper")

class MedicalInfo(Base):
    __tablename__ = "medical_info"
    
    id = Column(Integer, primary_key=True, index=True)
    camper_id = Column(Integer, ForeignKey("campers.id"), unique=True)
    blood_type = Column(String)
    allergies = Column(Text)
    medications = Column(Text)
    conditions = Column(Text)
    doctor_name = Column(String)
    doctor_phone = Column(String)
    insurance_provider = Column(String)
    insurance_policy = Column(String)
    dietary_restrictions = Column(Text)
    
    # Relationships
    camper = relationship("Camper", back_populates="medical_info")

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    
    id = Column(Integer, primary_key=True, index=True)
    camper_id = Column(Integer, ForeignKey("campers.id"))
    name = Column(String, nullable=False)
    relationship = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    alternate_phone = Column(String)
    is_primary = Column(Boolean, default=False)
    
    # Relationships
    camper = relationship("Camper", back_populates="emergency_contacts")