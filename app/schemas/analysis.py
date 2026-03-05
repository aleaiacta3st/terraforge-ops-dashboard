from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnalysisResponse(BaseModel):
    id: int
    incident_id: int
    risk_level: str
    contributing_factors: str
    recommendations: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AnalysisTriggerResponse(BaseModel):
    task_id: str
    incident_id: int
    status: str