from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.incident import SafetyIncident


@celery_app.task
def generate_safety_report(project_id: int):
    db = SessionLocal()
    try:
        incidents = db.query(SafetyIncident).filter(
            SafetyIncident.project_id == project_id
        ).all()

        severity_counts = {}
        type_counts = {}

        for incident in incidents:
            sev = incident.severity.value
            typ = incident.incident_type.value

            severity_counts[sev] = severity_counts.get(sev, 0) + 1
            type_counts[typ] = type_counts.get(typ, 0) + 1

        report = {
            "project_id": project_id,
            "total_incidents": len(incidents),
            "by_severity": severity_counts,
            "by_type": type_counts,
        }

        return report

    finally:
        db.close()