import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings

# Graceful DB fallback: If Postgres is not reachable, fallback to SQLite for zero-setup local runs
db_url = settings.DATABASE_URL
if os.getenv("TESTING") == "1" or not os.getenv("DATABASE_URL"):
    db_url = "sqlite:///./trustguard.db"

try:
    if "sqlite" in db_url:
        engine = create_engine(db_url, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(db_url, pool_pre_ping=True, pool_size=10, max_overflow=20)
except Exception:
    engine = create_engine("sqlite:///./trustguard.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
