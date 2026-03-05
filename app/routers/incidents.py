from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.incident import SafetyIncident
from app.schemas.incident import IncidentCreate, IncidentResponse, IncidentUpdate
from app.auth import get_current_user
from app.models.user import User 

from app.tasks import analyse_incident
from app.models.analysis import IncidentAnalysis
from app.schemas.analysis import AnalysisResponse, AnalysisTriggerResponse

router = APIRouter()


@router.get("/", response_model=list[IncidentResponse])
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(SafetyIncident).all()
    return incidents


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(SafetyIncident).filter(SafetyIncident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident


@router.post("/", response_model=IncidentResponse, status_code=201)
def create_incident(incident_data: IncidentCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    incident = SafetyIncident(**incident_data.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
def update_incident(incident_id: int, incident_data: IncidentUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    incident = db.query(SafetyIncident).filter(SafetyIncident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    for field, value in incident_data.model_dump(exclude_unset=True).items():
        setattr(incident, field, value)

    db.commit()
    db.refresh(incident)
    return incident


@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    incident = db.query(SafetyIncident).filter(SafetyIncident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    db.delete(incident)
    db.commit() 





@router.post("/{incident_id}/analyse", response_model=AnalysisTriggerResponse)
def trigger_analysis(incident_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    incident = db.query(SafetyIncident).filter(SafetyIncident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    task = analyse_incident.delay(incident_id)
    return {"task_id": task.id, "incident_id": incident_id, "status": "processing"}


@router.get("/{incident_id}/analyse", response_model=AnalysisResponse)
def get_analysis(incident_id: int, db: Session = Depends(get_db)):
    analysis = db.query(IncidentAnalysis).filter(IncidentAnalysis.incident_id == incident_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found. Trigger analysis first.")
    return analysis