# Terraforge Operations Dashboard

Internal operations and safety management dashboard for Terraforge Engineering Pvt Ltd.

## Stack

- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Database:** PostgreSQL 15
- **Cache/Queue:** Redis 7 + Celery
- **Frontend:** React (TBD)
- **Deployment:** Docker + Docker Compose

## Quick Start

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec api alembic upgrade head

# Seed the database
docker-compose exec api python -m app.seed

# API is at http://localhost:8000
# Docs at http://localhost:8000/docs
```

## Local Development (without Docker)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Make sure Postgres is running locally
alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

## Project Structure

```
app/
├── main.py          # FastAPI app entry point
├── config.py        # Environment config
├── database.py      # DB connection & session
├── seed.py          # Seed data script
├── models/          # SQLAlchemy models
├── schemas/         # Pydantic request/response schemas
├── routers/         # API route handlers
└── services/        # Business logic layer
```
