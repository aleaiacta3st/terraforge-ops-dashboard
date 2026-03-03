from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import projects, employees, incidents, equipment

app = FastAPI(
    title="Terraforge Operations Dashboard",
    description="Internal operations and safety management dashboard for Terraforge Engineering",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(employees.router, prefix="/employees", tags=["Employees"])
app.include_router(incidents.router, prefix="/incidents", tags=["Safety Incidents"])
app.include_router(equipment.router, prefix="/equipment", tags=["Equipment"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "terraforge-dashboard"}
