from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import date, datetime

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    role: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

# Parent Schemas
class ParentBase(BaseModel):
    phone: str
    address: str
    emergency_contact: str
    emergency_phone: str

class ParentCreate(ParentBase):
    user_id: int

class ParentResponse(ParentBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True

# Group Schemas
class GroupBase(BaseModel):
    name: str
    description: Optional[str] = None
    age_min: Optional[int] = None
    age_max: Optional[int] = None
    max_capacity: Optional[int] = None

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: int
    created_at: datetime
    camper_count: Optional[int] = 0
    
    class Config:
        from_attributes = True

# Emergency Contact Schemas
class EmergencyContactBase(BaseModel):
    name: str
    relationship: str
    phone: str
    alternate_phone: Optional[str] = None
    is_primary: bool = False

class EmergencyContactCreate(EmergencyContactBase):
    camper_id: int

class EmergencyContactResponse(EmergencyContactBase):
    id: int
    camper_id: int
    
    class Config:
        from_attributes = True

# Medical Info Schemas
class MedicalInfoBase(BaseModel):
    blood_type: Optional[str] = None
    allergies: Optional[str] = None
    medications: Optional[str] = None
    conditions: Optional[str] = None
    doctor_name: Optional[str] = None
    doctor_phone: Optional[str] = None
    insurance_provider: Optional[str] = None
    insurance_policy: Optional[str] = None
    dietary_restrictions: Optional[str] = None

class MedicalInfoCreate(MedicalInfoBase):
    camper_id: int

class MedicalInfoResponse(MedicalInfoBase):
    id: int
    camper_id: int
    
    class Config:
        from_attributes = True

# Camper Schemas
class CamperBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Optional[str] = None
    group_id: Optional[int] = None
    notes: Optional[str] = None

class CamperCreate(CamperBase):
    parent_ids: Optional[List[int]] = []
    emergency_contacts: Optional[List[EmergencyContactBase]] = []
    medical_info: Optional[MedicalInfoBase] = None

class CamperUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    group_id: Optional[int] = None
    is_active: Optional[bool] = None
    is_suspended: Optional[bool] = None
    notes: Optional[str] = None

class CamperResponse(CamperBase):
    id: int
    age: Optional[int] = None
    is_active: bool
    is_suspended: bool
    enrollment_date: date
    group: Optional[GroupResponse] = None
    parents: List[ParentResponse] = []
    medical_info: Optional[MedicalInfoResponse] = None
    emergency_contacts: List[EmergencyContactResponse] = []
    
    class Config:
        from_attributes = True
    
    @validator('age', always=True)
    def calculate_age(cls, v, values):
        if 'date_of_birth' in values:
            today = date.today()
            born = values['date_of_birth']
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return v