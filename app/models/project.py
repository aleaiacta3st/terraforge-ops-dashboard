import enum
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List

from sqlalchemy import String, Text, Date, DateTime, Numeric, Enum, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ProjectStatus(str, enum.Enum):
    PLANNING = "planning"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    DELAYED = "delayed"
    COMPLETED = "completed"


class ProjectType(str, enum.Enum):
    SHAFT_SINKING = "shaft_sinking"
    MINE_DEVELOPMENT = "mine_development"
    CONTRACT_MINING = "contract_mining"
    REHABILITATION = "rehabilitation"
    CONSTRUCTION = "construction"
    ELECTRICAL = "electrical"
    VENTILATION = "ventilation"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    project_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    client_name: Mapped[str] = mapped_column(String(255))
    site_location: Mapped[str] = mapped_column(String(255))
    project_type: Mapped[ProjectType] = mapped_column(Enum(ProjectType))
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus), default=ProjectStatus.PLANNING)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    start_date: Mapped[date] = mapped_column(Date)
    estimated_end_date: Mapped[date] = mapped_column(Date)
    actual_end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    budget: Mapped[Decimal] = mapped_column(Numeric(15, 2))
    spent: Mapped[Decimal] = mapped_column(Numeric(15, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    # Relationships
    employees: Mapped[List["Employee"]] = relationship("Employee", back_populates="project")
    incidents: Mapped[List["SafetyIncident"]] = relationship("SafetyIncident", back_populates="project")
    equipment: Mapped[List["Equipment"]] = relationship("Equipment", back_populates="project")
