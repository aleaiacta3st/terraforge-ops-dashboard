import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, Text, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class IncidentType(str, enum.Enum):
    NEAR_MISS = "near_miss"
    MINOR_INJURY = "minor_injury"
    MAJOR_INJURY = "major_injury"
    FATALITY = "fatality"
    EQUIPMENT_FAILURE = "equipment_failure"
    ENVIRONMENTAL = "environmental"
    STRUCTURAL = "structural"


class Severity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IncidentStatus(str, enum.Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"
    CLOSED = "closed"


class SafetyIncident(Base):
    __tablename__ = "safety_incidents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    incident_type: Mapped[IncidentType] = mapped_column(Enum(IncidentType))
    severity: Mapped[Severity] = mapped_column(Enum(Severity))
    status: Mapped[IncidentStatus] = mapped_column(Enum(IncidentStatus), default=IncidentStatus.OPEN)
    description: Mapped[str] = mapped_column(Text)
    resolution_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date_occurred: Mapped[date] = mapped_column(Date)
    date_reported: Mapped[date] = mapped_column(Date)

    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id"), index=True)
    reported_by_id: Mapped[int] = mapped_column(ForeignKey("employees.id"))

    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    project: Mapped["Project"] = relationship("Project", back_populates="incidents")
    reported_by_employee: Mapped["Employee"] = relationship("Employee", back_populates="reported_incidents")
