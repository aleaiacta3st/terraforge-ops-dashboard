from celery import Celery
from app.config import REDIS_URL

celery_app = Celery(
    "terraforge",
    broker=REDIS_URL, #fastapi posts tasks here
    backend=REDIS_URL, #celery posts results of the tasks here. redis plays a dual role.
    include=["app.tasks"],
)