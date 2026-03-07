from app.database import SessionLocal
from app.models.incident import SafetyIncident
from app.services.embeddings import get_embedding


def backfill():
    db = SessionLocal()
    try:
        incidents = db.query(SafetyIncident).filter(SafetyIncident.embedding == None).all()
        print(f"Found {len(incidents)} incidents without embeddings")

        for incident in incidents:
            text = f"{incident.title}. {incident.description}"
            incident.embedding = get_embedding(text)
            print(f"  Embedded incident #{incident.id}: {incident.title}")

        db.commit()
        print("Done!")
    finally:
        db.close()


if __name__ == "__main__":
    backfill()