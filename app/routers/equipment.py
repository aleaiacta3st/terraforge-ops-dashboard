from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.equipment import Equipment
from app.schemas.equipment import EquipmentCreate, EquipmentResponse, EquipmentUpdate
from app.auth import get_current_user
from app.models.user import User


router = APIRouter()


@router.get("/", response_model=list[EquipmentResponse])
def get_equipment(db: Session = Depends(get_db)):
    equipment = db.query(Equipment).all()
    return equipment


@router.get("/{equipment_id}", response_model=EquipmentResponse)
def get_equipment_item(equipment_id: int, db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")
    return equipment


@router.post("/", response_model=EquipmentResponse, status_code=201)
def create_equipment(equipment_data: EquipmentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    equipment = Equipment(**equipment_data.model_dump())
    db.add(equipment)
    db.commit()
    db.refresh(equipment)
    return equipment


@router.put("/{equipment_id}", response_model=EquipmentResponse)
def update_equipment(equipment_id: int, equipment_data: EquipmentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    for field, value in equipment_data.model_dump(exclude_unset=True).items():
        setattr(equipment, field, value)

    db.commit()
    db.refresh(equipment)
    return equipment


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(equipment_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    equipment = db.query(Equipment).filter(Equipment.id == equipment_id).first()
    if not equipment:
        raise HTTPException(status_code=404, detail="Equipment not found")

    db.delete(equipment)
    db.commit()