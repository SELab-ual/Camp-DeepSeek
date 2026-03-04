from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Parent, User, Camper
from schemas import ParentCreate, ParentResponse
from auth import require_role

router = APIRouter()

@router.post("/", response_model=ParentResponse)
async def create_parent(
    parent: ParentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    db_parent = Parent(**parent.model_dump())
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

@router.get("/", response_model=List[ParentResponse])
async def read_parents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    parents = db.query(Parent).offset(skip).limit(limit).all()
    return parents

@router.get("/{parent_id}", response_model=ParentResponse)
async def read_parent(
    parent_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return parent

@router.put("/{parent_id}", response_model=ParentResponse)
async def update_parent(
    parent_id: int,
    parent_update: ParentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    for key, value in parent_update.model_dump().items():
        setattr(parent, key, value)
    
    db.commit()
    db.refresh(parent)
    return parent

@router.delete("/{parent_id}")
async def delete_parent(
    parent_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    db.delete(parent)
    db.commit()
    return {"message": "Parent deleted successfully"}

@router.get("/{parent_id}/campers")
async def get_parent_campers(
    parent_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    parent = db.query(Parent).filter(Parent.id == parent_id).first()
    if not parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    
    campers = parent.campers
    return [{"id": c.id, "name": f"{c.first_name} {c.last_name}"} for c in campers]