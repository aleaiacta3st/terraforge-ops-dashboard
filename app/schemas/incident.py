from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from app.models.incident import IncidentType, Severity, IncidentStatus


class IncidentCreate(BaseModel):
    title: str
    incident_type: IncidentType
    severity: Severity
    description: str
    date_occurred: date
    date_reported: date
    project_id: int
    reported_by_id: int
    status: Optional[IncidentStatus] = IncidentStatus.OPEN
    resolution_notes: Optional[str] = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    incident_type: IncidentType
    severity: Severity
    status: IncidentStatus
    description: str
    resolution_notes: Optional[str] = None
    date_occurred: date
    date_reported: date
    project_id: int
    reported_by_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class IncidentUpdate(BaseModel):
    title: Optional[str] = None
    incident_type: Optional[IncidentType] = None
    severity: Optional[Severity] = None
    status: Optional[IncidentStatus] = None
    description: Optional[str] = None
    resolution_notes: Optional[str] = None
    date_occurred: Optional[date] = None
    date_reported: Optional[date] = None
    project_id: Optional[int] = None
    reported_by_id: Optional[int] = None