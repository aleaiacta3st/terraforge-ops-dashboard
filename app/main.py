from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import projects, employees, incidents, equipment, auth, reports
import os

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
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "terraforge-dashboard"}

# Serve React static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(static_dir, "assets")), name="static-assets")

    @app.get("/{full_path:path}")
    def serve_react(full_path: str):
        # Check if the file exists in static directory
        file_path = os.path.join(static_dir, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(static_dir, "index.html"))
