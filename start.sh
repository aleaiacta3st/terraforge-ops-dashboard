#!/bin/bash
alembic upgrade head
python -m app.seed
celery -A app.celery_app:celery_app worker --loglevel=info --concurrency=2 --pool=solo &
uvicorn app.main:app --host 0.0.0.0 --port 8000