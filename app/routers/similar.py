from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.incident import SafetyIncident
from app.schemas.incident import IncidentResponse

router = APIRouter()


@router.get("/{incident_id}/similar", response_model=list[IncidentResponse])
def get_similar_incidents(incident_id: int, db: Session = Depends(get_db)):
    # Get the incident we want to find similar ones for
    incident = db.query(SafetyIncident).filter(SafetyIncident.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    if incident.embedding is None:
        raise HTTPException(status_code=400, detail="Incident has no embedding")

    # Find the 3 most similar incidents using pgvector's distance operator
    similar = (
        db.query(SafetyIncident)
        .filter(SafetyIncident.id != incident_id)
        .filter(SafetyIncident.embedding != None)
        .order_by(SafetyIncident.embedding.cosine_distance(incident.embedding))
        .limit(3)
        .all()
    )

    return similar