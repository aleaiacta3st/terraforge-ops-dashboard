import anthropic

from app.celery_app import celery_app
from app.config import ANTHROPIC_API_KEY
from app.database import SessionLocal
from app.models.incident import SafetyIncident
from app.models.analysis import IncidentAnalysis
from app.services.embeddings import get_embedding


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


@celery_app.task
def analyse_incident(incident_id: int):
    db = SessionLocal()
    try:
        # fetch incident and its related data
        incident = db.query(SafetyIncident).filter(SafetyIncident.id == incident_id).first()
        if not incident:
            return {"error": "Incident not found"}

        # Generate embedding if missing
        if incident.embedding is None:
            text = f"{incident.title}. {incident.description}"
            incident.embedding = get_embedding(text)
            db.commit()

        # Find similar past incidents using embeddings (RAG retrieval step)
        similar_context = ""
        similar = (
            db.query(SafetyIncident)
            .filter(SafetyIncident.id != incident_id)
            .filter(SafetyIncident.embedding != None)
            .order_by(SafetyIncident.embedding.cosine_distance(incident.embedding))
            .limit(3)
            .all()
        )
        if similar:
            similar_context = "\n\nSimilar Past Incidents:\n"
            for i, s in enumerate(similar, 1):
                similar_context += f"{i}. {s.title} (Severity: {s.severity.value}, Type: {s.incident_type.value}, Project: {s.project.name})\n"

        # build the prompt using real data + similar incidents (RAG augmentation step)
        prompt = f"""You are a mining safety expert. Analyse the following safety incident and provide a structured assessment.

Incident Title: {incident.title}
Incident Type: {incident.incident_type.value}
Severity: {incident.severity.value}
Status: {incident.status.value}
Date Occurred: {incident.date_occurred}
Project: {incident.project.name}
Site Location: {incident.project.site_location}
Project Type: {incident.project.project_type.value}
Reported By: {incident.reported_by_employee.full_name} ({incident.reported_by_employee.role.value})
Description: {incident.description}
{similar_context}
Respond in exactly this format with no extra text:

RISK_LEVEL: [one of: Low, Medium, High, Critical]

CONTRIBUTING_FACTORS: [a concise paragraph identifying the key contributing factors]

RECOMMENDATIONS: [a concise paragraph with specific corrective actions and preventive measures]"""

        # call the Claude API (RAG generation step)
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        raw_response = message.content[0].text

        # parse the structured response
        risk_level = ""
        contributing_factors = ""
        recommendations = ""

        for line in raw_response.split("\n"):
            if line.startswith("RISK_LEVEL:"):
                risk_level = line.replace("RISK_LEVEL:", "").strip()
            elif line.startswith("CONTRIBUTING_FACTORS:"):
                contributing_factors = line.replace("CONTRIBUTING_FACTORS:", "").strip()
            elif line.startswith("RECOMMENDATIONS:"):
                recommendations = line.replace("RECOMMENDATIONS:", "").strip()

        # save to the database
        analysis = IncidentAnalysis(
            incident_id=incident_id,
            risk_level=risk_level,
            contributing_factors=contributing_factors,
            recommendations=recommendations,
            raw_response=raw_response,
        )
        db.add(analysis)
        db.commit()

        return {"incident_id": incident_id, "status": "completed"}

    finally:
        db.close()