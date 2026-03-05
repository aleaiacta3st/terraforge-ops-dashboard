from datetime import datetime
from typing import Optional

from sqlalchemy import Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class IncidentAnalysis(Base):
    __tablename__ = "incident_analyses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    incident_id: Mapped[int] = mapped_column(ForeignKey("safety_incidents.id"), unique=True, index=True)
    risk_level: Mapped[str] = mapped_column(Text)
    contributing_factors: Mapped[str] = mapped_column(Text)
    recommendations: Mapped[str] = mapped_column(Text)
    raw_response: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationship
    incident: Mapped["SafetyIncident"] = relationship("SafetyIncident", back_populates="analysis")