"""
Database Utilities
PostgreSQL database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from typing import Generator
import os


# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/littlemonster"
)

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    echo=os.getenv("SQL_ECHO", "false").lower() == "true"
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db_url() -> str:
    """Get database URL from environment"""
    return DATABASE_URL


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Get a database session with context management
    
    Usage:
        with get_db_session() as db:
            user = db.query(User).filter(User.id == user_id).first()
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database sessions
    
    Usage:
        @app.get("/users/{user_id}")
        async def get_user(user_id: int, db: Session = Depends(get_db)):
            return db.query(User).filter(User.id == user_id).first()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
