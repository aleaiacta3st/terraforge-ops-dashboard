#!/bin/bash
alembic upgrade head
python -m app.seed
celery -A app.celery_app:celery_app worker --loglevel=info &
uvicorn app.main:app --host 0.0.0.0 --port 8000