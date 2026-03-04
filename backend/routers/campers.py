from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Camper, Parent, Group, EmergencyContact, MedicalInfo
from schemas import CamperCreate, CamperResponse, CamperUpdate
from auth import require_role

router = APIRouter()

@router.post("/", response_model=CamperResponse)
async def create_camper(
    camper: CamperCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    # Create camper
    db_camper = Camper(
        first_name=camper.first_name,
        last_name=camper.last_name,
        date_of_birth=camper.date_of_birth,
        gender=camper.gender,
        group_id=camper.group_id,
        notes=camper.notes
    )
    db.add(db_camper)
    db.flush()  # Get ID without committing
    
    # Add parents if provided
    if camper.parent_ids:
        parents = db.query(Parent).filter(Parent.id.in_(camper.parent_ids)).all()
        db_camper.parents.extend(parents)
    
    # Add emergency contacts
    if camper.emergency_contacts:
        for contact in camper.emergency_contacts:
            db_contact = EmergencyContact(
                camper_id=db_camper.id,
                **contact.model_dump()
            )
            db.add(db_contact)
    
    # Add medical info
    if camper.medical_info:
        db_medical = MedicalInfo(
            camper_id=db_camper.id,
            **camper.medical_info.model_dump()
        )
        db.add(db_medical)
    
    db.commit()
    db.refresh(db_camper)
    return db_camper

@router.get("/", response_model=List[CamperResponse])
async def read_campers(
    skip: int = 0,
    limit: int = 100,
    group_id: int = None,
    is_active: bool = None,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    query = db.query(Camper)
    
    if group_id:
        query = query.filter(Camper.group_id == group_id)
    if is_active is not None:
        query = query.filter(Camper.is_active == is_active)
    
    campers = query.offset(skip).limit(limit).all()
    return campers

@router.get("/{camper_id}", response_model=CamperResponse)
async def read_camper(
    camper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    camper = db.query(Camper).filter(Camper.id == camper_id).first()
    if not camper:
        raise HTTPException(status_code=404, detail="Camper not found")
    return camper

@router.put("/{camper_id}", response_model=CamperResponse)
async def update_camper(
    camper_id: int,
    camper_update: CamperUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    camper = db.query(Camper).filter(Camper.id == camper_id).first()
    if not camper:
        raise HTTPException(status_code=404, detail="Camper not found")
    
    for key, value in camper_update.model_dump(exclude_unset=True).items():
        setattr(camper, key, value)
    
    db.commit()
    db.refresh(camper)
    return camper

@router.delete("/{camper_id}")
async def delete_camper(
    camper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    camper = db.query(Camper).filter(Camper.id == camper_id).first()
    if not camper:
        raise HTTPException(status_code=404, detail="Camper not found")
    
    db.delete(camper)
    db.commit()
    return {"message": "Camper deleted successfully"}

@router.post("/{camper_id}/suspend")
async def suspend_camper(
    camper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    camper = db.query(Camper).filter(Camper.id == camper_id).first()
    if not camper:
        raise HTTPException(status_code=404, detail="Camper not found")
    
    camper.is_suspended = True
    db.commit()
    return {"message": "Camper suspended successfully"}

@router.post("/{camper_id}/activate")
async def activate_camper(
    camper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    camper = db.query(Camper).filter(Camper.id == camper_id).first()
    if not camper:
        raise HTTPException(status_code=404, detail="Camper not found")
    
    camper.is_suspended = False
    db.commit()
    return {"message": "Camper activated successfully"}