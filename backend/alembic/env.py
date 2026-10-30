import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("FRONTEND_DIR", ".")
from alembic import context
from app.main import Base, engine_db   # uses DATABASE_URL / JWT_SECRET env vars
with engine_db.connect() as c:
    context.configure(connection=c, target_metadata=Base.metadata)
    with context.begin_transaction(): context.run_migrations()
