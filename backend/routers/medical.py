from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import MedicalInfo, Camper
from schemas import MedicalInfoCreate, MedicalInfoResponse
from auth import require_role

router = APIRouter()

@router.post("/", response_model=MedicalInfoResponse)
async def create_medical_info(
    medical: MedicalInfoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    # Check if camper exists
    camper = db.query(Camper).filter(Camper.id == medical.camper_id).first()
    if not camper:
        raise HTTPException(status_code=404, detail="Camper not found")
    
    # Check if medical info already exists for this camper
    existing = db.query(MedicalInfo).filter(MedicalInfo.camper_id == medical.camper_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Medical info already exists for this camper"
        )
    
    db_medical = MedicalInfo(**medical.model_dump())
    db.add(db_medical)
    db.commit()
    db.refresh(db_medical)
    return db_medical

@router.get("/camper/{camper_id}", response_model=MedicalInfoResponse)
async def read_medical_info(
    camper_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    medical = db.query(MedicalInfo).filter(MedicalInfo.camper_id == camper_id).first()
    if not medical:
        raise HTTPException(status_code=404, detail="Medical information not found")
    return medical

@router.put("/{medical_id}", response_model=MedicalInfoResponse)
async def update_medical_info(
    medical_id: int,
    medical_update: MedicalInfoCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    medical = db.query(MedicalInfo).filter(MedicalInfo.id == medical_id).first()
    if not medical:
        raise HTTPException(status_code=404, detail="Medical information not found")
    
    for key, value in medical_update.model_dump().items():
        setattr(medical, key, value)
    
    db.commit()
    db.refresh(medical)
    return medical

@router.delete("/{medical_id}")
async def delete_medical_info(
    medical_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    medical = db.query(MedicalInfo).filter(MedicalInfo.id == medical_id).first()
    if not medical:
        raise HTTPException(status_code=404, detail="Medical information not found")
    
    db.delete(medical)
    db.commit()
    return {"message": "Medical information deleted successfully"}