# Supplement Guidance Platform — Backend

Flow: React (Vite, Axios) -> FastAPI `/api/*` (JWT Bearer) -> SQLAlchemy -> PostgreSQL/Supabase / SQLite -> deterministic engine (`app/algorithms/engine.py`) -> JSON -> Results page. Each run stores a frozen profile snapshot + dataset/rule/scoring versions.

## Setup & Running (Windows PowerShell)

```powershell
# 1. Environment variables
$env:JWT_SECRET = python -c "import secrets; print(secrets.token_urlsafe(48))"
$env:DATA_DIR = "data_verified"
# Optional PostgreSQL: $env:DATABASE_URL = "postgresql+psycopg://..." (defaults to sqlite:///./app.db)

# 2. Dependencies
pip install -r requirements.txt

# 3. Database migrations (Alembic)
alembic upgrade head

# 4. Repeatable Knowledge Base Import (130 supplements)
python -m app.data_importer data_verified

# 5. Run automated tests (34 passing tests)
python -m pytest -v

# 6. Start API server
uvicorn app.main:app --reload --port 8000
```

## Features Implemented
- Full SQLAlchemy ORM models in `app/models.py` covering all 19 knowledge base tables and 4 application tables.
- Alembic migrations (`0001_initial.py` and `0002_knowledge_base.py`) compatible with both SQLite and PostgreSQL.
- Repeatable idempotent dataset importer (`app/data_importer.py`) with primary-key upsert support across all 19 tables.
- 8-stage deterministic recommendation algorithm with safety pre-filtering, WSM scoring ($0.40G + 0.20D + 0.15A + 0.15L + 0.10H$), threshold filtering ($\ge 0.60$), and deterministic ranking.
- Rule R000 enforcement: unverified candidates are strictly routed to `needs_review` and withheld from recommendations.
- Frozen historical snapshots stored in `recommendation_runs` and individual candidate results in `recommendation_results`.
- Reliable path resolution in `app/data_loader.py` and `app/main.py` ensuring files load seamlessly whether run from root or `backend/`.
- 34 automated pytest tests passing with 0 errors across API endpoints, WSM calculations, catalogue filtering, and safety exclusions.
