from pydantic import BaseModel
from datetime import date,datetime
from decimal import Decimal
from typing import Optional

from app.models.project import ProjectType, ProjectStatus


class ProjectCreate(BaseModel):
    name: str
    project_code: str
    client_name: str
    site_location: str
    project_type: ProjectType
    start_date: date
    estimated_end_date: date
    budget: Decimal
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.PLANNING 





class ProjectResponse(BaseModel):
    id: int
    name: str
    project_code: str
    client_name: str
    site_location: str
    project_type: ProjectType
    status: ProjectStatus
    description: Optional[str] = None
    start_date: date
    estimated_end_date: date
    actual_end_date: Optional[date] = None
    budget: Decimal
    spent: Decimal
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True} 




class ProjectUpdate(BaseModel):
    name: str | None = None
    project_code: str | None = None
    client_name: str | None = None
    site_location: str | None = None
    project_type: ProjectType | None = None
    status: ProjectStatus | None = None
    description: str | None = None
    start_date: date | None = None
    estimated_end_date: date | None = None
    actual_end_date: date | None = None
    budget: Decimal | None = None
    spent: Decimal | None = None