"""
Seed the database with realistic Terraforge Engineering data.
Run: python -m app.seed
"""
from datetime import date, timedelta
import random

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import (
    User, UserRole,
    Project, ProjectStatus, ProjectType,
    Employee, EmployeeRole,
    SafetyIncident, IncidentType, Severity, IncidentStatus,
    Equipment, EquipmentStatus,
)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed():
    db: Session = SessionLocal()

    # Check if already seeded
    if db.query(User).count() > 0:
        print("Database already seeded. Skipping.")
        db.close()
        return

    print("Seeding database...")

    # ── Users (dashboard users, not all 600 employees) ──
    users = [
        User(email="admin@terraforgeeng.com", username="admin", hashed_password=pwd_context.hash("admin123"), full_name="Arjun Mehta", role=UserRole.ADMIN),
        User(email="safety@terraforgeeng.com", username="safety_lead", hashed_password=pwd_context.hash("safety123"), full_name="Rajesh Kumar", role=UserRole.SAFETY_OFFICER),
        User(email="pm@terraforgeeng.com", username="pm_anil", hashed_password=pwd_context.hash("pm123"), full_name="Anil Rao", role=UserRole.MANAGER),
        User(email="eng@terraforgeeng.com", username="eng_priya", hashed_password=pwd_context.hash("eng123"), full_name="Priya Sharma", role=UserRole.ENGINEER),
        User(email="viewer@terraforgeeng.com", username="viewer", hashed_password=pwd_context.hash("viewer123"), full_name="Sudheer Nair", role=UserRole.VIEWER),
    ]
    db.add_all(users)
    db.flush()

    # ── Projects ──
    projects = [
        Project(
            name="Kolar Gold Fields - Shaft Deepening",
            project_code="KGF-2024-001",
            client_name="Bharat Gold Mines Ltd",
            site_location="Kolar, Karnataka",
            project_type=ProjectType.SHAFT_SINKING,
            status=ProjectStatus.ACTIVE,
            description="Deepening of main production shaft from 800m to 1200m depth with full equipping",
            start_date=date(2024, 3, 1),
            estimated_end_date=date(2025, 8, 31),
            budget=450000000,
            spent=287000000,
        ),
        Project(
            name="Singareni - Ventilation Upgrade",
            project_code="SCCL-2024-002",
            client_name="Singareni Collieries Company Ltd",
            site_location="Ramagundam, Telangana",
            project_type=ProjectType.VENTILATION,
            status=ProjectStatus.ACTIVE,
            description="Installation and commissioning of new main ventilation fans for underground coal mine",
            start_date=date(2024, 6, 15),
            estimated_end_date=date(2025, 3, 31),
            budget=85000000,
            spent=52000000,
        ),
        Project(
            name="Hindustan Zinc - Underground Development",
            project_code="HZL-2024-003",
            client_name="Hindustan Zinc Ltd",
            site_location="Rajpura Dariba, Rajasthan",
            project_type=ProjectType.MINE_DEVELOPMENT,
            status=ProjectStatus.DELAYED,
            description="Development of 3km decline and associated underground infrastructure",
            start_date=date(2024, 1, 10),
            estimated_end_date=date(2025, 6, 30),
            budget=320000000,
            spent=198000000,
        ),
        Project(
            name="NMDC - Electrical Systems Overhaul",
            project_code="NMDC-2024-004",
            client_name="NMDC Limited",
            site_location="Kirandul, Chhattisgarh",
            project_type=ProjectType.ELECTRICAL,
            status=ProjectStatus.ACTIVE,
            description="Complete replacement of underground electrical distribution and instrumentation systems",
            start_date=date(2024, 9, 1),
            estimated_end_date=date(2025, 12, 31),
            budget=120000000,
            spent=31000000,
        ),
        Project(
            name="Tata Steel - Mine Rehabilitation",
            project_code="TATA-2023-005",
            client_name="Tata Steel Mining Ltd",
            site_location="West Bokaro, Jharkhand",
            project_type=ProjectType.REHABILITATION,
            status=ProjectStatus.COMPLETED,
            description="Rehabilitation of abandoned iron ore mine including structural reinforcement and water management",
            start_date=date(2023, 4, 1),
            estimated_end_date=date(2024, 9, 30),
            actual_end_date=date(2024, 11, 15),
            budget=200000000,
            spent=215000000,
        ),
        Project(
            name="Coal India - Contract Mining Operations",
            project_code="CIL-2025-006",
            client_name="Coal India Limited",
            site_location="Dhanbad, Jharkhand",
            project_type=ProjectType.CONTRACT_MINING,
            status=ProjectStatus.PLANNING,
            description="2-year contract mining operation for new underground coal seam",
            start_date=date(2025, 4, 1),
            estimated_end_date=date(2027, 3, 31),
            budget=680000000,
            spent=0,
        ),
    ]
    db.add_all(projects)
    db.flush()

    # ── Employees (sample of the 600) ──
    first_names = ["Ravi", "Suresh", "Amit", "Vikram", "Deepak", "Sanjay", "Manoj", "Arun", "Kiran", "Rahul",
                   "Priya", "Anita", "Lakshmi", "Sunita", "Kavitha", "Ramesh", "Gopal", "Venkat", "Naresh", "Bhanu",
                   "Srinivas", "Mahesh", "Rajendra", "Prakash", "Sunil", "Ganesh", "Harish", "Mohan", "Dinesh", "Satish"]
    last_names = ["Reddy", "Sharma", "Kumar", "Singh", "Patel", "Rao", "Verma", "Gupta", "Nair", "Pillai",
                  "Choudhary", "Mishra", "Das", "Joshi", "Tiwari"]

    employees = []
    roles_list = list(EmployeeRole)
    for i in range(60):
        fname = random.choice(first_names)
        lname = random.choice(last_names)
        role = random.choice(roles_list)
        proj = random.choice(projects[:5]) if random.random() > 0.1 else None  # 10% unassigned

        emp = Employee(
            employee_code=f"GE-{1001 + i}",
            full_name=f"{fname} {lname}",
            email=f"{fname.lower()}.{lname.lower()}{i}@terraforgeeng.com",
            phone=f"+91-{random.randint(70000, 99999)}{random.randint(10000, 99999)}",
            role=role,
            project_id=proj.id if proj else None,
            hire_date=date(2020, 1, 1) + timedelta(days=random.randint(0, 1800)),
            is_active=random.random() > 0.05,
        )
        employees.append(emp)
    db.add_all(employees)
    db.flush()

    # ── Safety Incidents ──
    incident_titles = {
        IncidentType.NEAR_MISS: ["Rock fall in tunnel section", "Unsecured scaffolding detected", "Gas reading spike in shaft", "Vehicle near-collision at portal", "Loose bolt on conveyor guard"],
        IncidentType.MINOR_INJURY: ["Hand laceration during bolt installation", "Twisted ankle on uneven ground", "Minor burn from welding splatter", "Bruised shoulder from falling debris"],
        IncidentType.MAJOR_INJURY: ["Fractured arm from equipment malfunction", "Crush injury during shaft lining"],
        IncidentType.EQUIPMENT_FAILURE: ["Hoist motor failure at 600m depth", "Ventilation fan bearing seizure", "Conveyor belt tear", "Pump failure causing water accumulation"],
        IncidentType.ENVIRONMENTAL: ["Diesel spill near portal", "Excessive dust levels in decline", "Water table breach during drilling"],
        IncidentType.STRUCTURAL: ["Tunnel support displacement detected", "Crack in shaft lining at 450m"],
    }

    active_employees = [e for e in employees if e.is_active and e.project_id is not None]
    incidents = []
    for i in range(25):
        inc_type = random.choice(list(incident_titles.keys()))
        title = random.choice(incident_titles[inc_type])
        reporter = random.choice(active_employees)
        days_ago = random.randint(1, 365)
        occurred = date.today() - timedelta(days=days_ago)
        reported = occurred + timedelta(days=random.randint(0, 2))

        severity_map = {
            IncidentType.NEAR_MISS: [Severity.LOW, Severity.MEDIUM],
            IncidentType.MINOR_INJURY: [Severity.LOW, Severity.MEDIUM],
            IncidentType.MAJOR_INJURY: [Severity.HIGH, Severity.CRITICAL],
            IncidentType.EQUIPMENT_FAILURE: [Severity.MEDIUM, Severity.HIGH],
            IncidentType.ENVIRONMENTAL: [Severity.MEDIUM, Severity.HIGH],
            IncidentType.STRUCTURAL: [Severity.HIGH, Severity.CRITICAL],
        }

        status = random.choice(list(IncidentStatus))
        resolution = f"Investigation completed. Corrective action implemented." if status in [IncidentStatus.RESOLVED, IncidentStatus.CLOSED] else None

        inc = SafetyIncident(
            title=title,
            incident_type=inc_type,
            severity=random.choice(severity_map[inc_type]),
            status=status,
            description=f"{title}. Occurred during routine operations at site. Immediate area was secured and supervisor notified.",
            resolution_notes=resolution,
            date_occurred=occurred,
            date_reported=reported,
            project_id=reporter.project_id,
            reported_by_id=reporter.id,
        )
        incidents.append(inc)
    db.add_all(incidents)

    # ── Equipment ──
    equipment_data = [
        ("Winder Drum Hoist", "hoist", "WDH"), ("Mucker Machine", "excavation", "MCK"),
        ("Rock Bolter", "support", "RBT"), ("Shotcrete Sprayer", "support", "SCS"),
        ("Underground Truck", "transport", "UTK"), ("LHD Loader", "excavation", "LHD"),
        ("Ventilation Fan", "ventilation", "VFN"), ("Dewatering Pump", "pump", "DWP"),
        ("Drill Jumbo", "drilling", "DJB"), ("Conveyor Belt System", "transport", "CBS"),
        ("Man Cage", "transport", "MCG"), ("Kibble Bucket", "shaft_sinking", "KBL"),
        ("Headgear Crane", "lifting", "HGC"), ("Grout Pump", "grouting", "GRP"),
        ("Diesel Generator", "power", "DGN"),
    ]

    equipment_items = []
    statuses = list(EquipmentStatus)
    for idx, (name, eq_type, prefix) in enumerate(equipment_data):
        for copy in range(random.randint(1, 3)):
            proj = random.choice(projects[:5])
            maint_date = date.today() - timedelta(days=random.randint(10, 180))
            eq = Equipment(
                name=f"{name} #{copy + 1}",
                equipment_type=eq_type,
                serial_number=f"{prefix}-{2024}-{idx:03d}-{copy:02d}",
                status=random.choices(statuses, weights=[70, 15, 10, 5])[0],
                project_id=proj.id,
                last_maintenance_date=maint_date,
                next_maintenance_due=maint_date + timedelta(days=90),
                purchase_date=date(2020, 1, 1) + timedelta(days=random.randint(0, 1500)),
            )
            equipment_items.append(eq)
    db.add_all(equipment_items)

    db.commit()
    db.close()
    print("Seeding complete!")
    print(f"  Users: {len(users)}")
    print(f"  Projects: {len(projects)}")
    print(f"  Employees: {len(employees)}")
    print(f"  Safety Incidents: {len(incidents)}")
    print(f"  Equipment: {len(equipment_items)}")


if __name__ == "__main__":
    seed()
