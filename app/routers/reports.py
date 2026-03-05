from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult

from app.tasks import generate_safety_report
from app.celery_app import celery_app

router = APIRouter()


@router.post("/safety/{project_id}")
def request_safety_report(project_id: int):
    task = generate_safety_report.delay(project_id)
    return {"task_id": task.id, "status": "processing"}


@router.get("/status/{task_id}")
def get_report_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)

    if result.ready():
        return {"task_id": task_id, "status": "completed", "result": result.get()}
    else:
        return {"task_id": task_id, "status": "processing"}