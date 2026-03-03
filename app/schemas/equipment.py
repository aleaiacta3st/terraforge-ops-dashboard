from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from app.models.equipment import EquipmentStatus


class EquipmentCreate(BaseModel):
    name: str
    equipment_type: str
    serial_number: str
    project_id: Optional[int] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_due: Optional[date] = None
    purchase_date: Optional[date] = None
    status: Optional[EquipmentStatus] = EquipmentStatus.OPERATIONAL


class EquipmentResponse(BaseModel):
    id: int
    name: str
    equipment_type: str
    serial_number: str
    status: EquipmentStatus
    project_id: Optional[int] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_due: Optional[date] = None
    purchase_date: Optional[date] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class EquipmentUpdate(BaseModel):
    name: Optional[str] = None
    equipment_type: Optional[str] = None
    serial_number: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    project_id: Optional[int] = None
    last_maintenance_date: Optional[date] = None
    next_maintenance_due: Optional[date] = None
    purchase_date: Optional[date] = None