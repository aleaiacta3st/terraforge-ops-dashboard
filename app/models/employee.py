import enum
from datetime import date, datetime
from typing import Optional, List

from sqlalchemy import String, Date, DateTime, Boolean, Enum, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EmployeeRole(str, enum.Enum):
    SITE_ENGINEER = "site_engineer"
    OPERATOR = "operator"
    SAFETY_OFFICER = "safety_officer"
    FOREMAN = "foreman"
    ELECTRICIAN = "electrician"
    MECHANIC = "mechanic"
    GEOLOGIST = "geologist"
    PROJECT_MANAGER = "project_manager"
    GENERAL_WORKER = "general_worker"


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_code: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    role: Mapped[EmployeeRole] = mapped_column(Enum(EmployeeRole))
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id"), nullable=True)
    hire_date: Mapped[date] = mapped_column(Date)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    # Relationships
    project: Mapped[Optional["Project"]] = relationship("Project", back_populates="employees")
    reported_incidents: Mapped[List["SafetyIncident"]] = relationship("SafetyIncident", back_populates="reported_by_employee")
