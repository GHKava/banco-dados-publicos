"""
Database engine and session management.

Provides SQLAlchemy engine creation and session factory for Postgres connections.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Database URL from environment (fallback to local dev)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/public_db")


def get_engine():
    """
    Create and return SQLAlchemy engine.

    Returns:
        Engine: SQLAlchemy engine instance
    """
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Set True for SQL logging
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,  # Verify connections before use
    )
    return engine


def get_session() -> Generator[Session, None, None]:
    """
    Create database session (generator for dependency injection).

    Yields:
        Session: SQLAlchemy session instance

    Example:
        >>> with next(get_session()) as session:
        ...     sources = session.query(Source).all()
    """
    engine = get_engine()
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
