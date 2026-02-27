import enum
from datetime import date, datetime
from typing import Optional

from sqlalchemy import String, Date, DateTime, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EquipmentStatus(str, enum.Enum):
    OPERATIONAL = "operational"
    MAINTENANCE = "maintenance"
    BROKEN = "broken"
    DECOMMISSIONED = "decommissioned"


class Equipment(Base):
    __tablename__ = "equipment"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    equipment_type: Mapped[str] = mapped_column(String(100))
    serial_number: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[EquipmentStatus] = mapped_column(Enum(EquipmentStatus), default=EquipmentStatus.OPERATIONAL)
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    last_maintenance_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    next_maintenance_due: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    purchase_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="equipment")
