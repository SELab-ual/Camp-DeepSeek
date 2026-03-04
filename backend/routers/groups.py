from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Group, Camper
from schemas import GroupCreate, GroupResponse
from auth import require_role

router = APIRouter()

@router.post("/", response_model=GroupResponse)
async def create_group(
    group: GroupCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    # Check if group name already exists
    existing = db.query(Group).filter(Group.name == group.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group name already exists"
        )
    
    db_group = Group(**group.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/", response_model=List[GroupResponse])
async def read_groups(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    groups = db.query(Group).offset(skip).limit(limit).all()
    
    # Add camper count
    for group in groups:
        group.camper_count = db.query(Camper).filter(Camper.group_id == group.id).count()
    
    return groups

@router.get("/{group_id}", response_model=GroupResponse)
async def read_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    group.camper_count = db.query(Camper).filter(Camper.group_id == group.id).count()
    return group

@router.put("/{group_id}", response_model=GroupResponse)
async def update_group(
    group_id: int,
    group_update: GroupCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check name uniqueness if changed
    if group_update.name != group.name:
        existing = db.query(Group).filter(Group.name == group_update.name).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Group name already exists"
            )
    
    for key, value in group_update.model_dump().items():
        setattr(group, key, value)
    
    db.commit()
    db.refresh(group)
    return group

@router.delete("/{group_id}")
async def delete_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Check if group has campers
    camper_count = db.query(Camper).filter(Camper.group_id == group_id).count()
    if camper_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete group with {camper_count} campers assigned"
        )
    
    db.delete(group)
    db.commit()
    return {"message": "Group deleted successfully"}

@router.get("/{group_id}/campers")
async def get_group_campers(
    group_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_role("admin"))
):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    campers = db.query(Camper).filter(Camper.group_id == group_id).all()
    return [{"id": c.id, "name": f"{c.first_name} {c.last_name}"} for c in campers]