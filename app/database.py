import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Default database (can be overridden by ENV variable)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/vortexai"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
