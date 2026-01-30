"""
Database package for Banco de Dados Interrelacional.

Provides PostgreSQL + pgvector schema, models, and utilities.
"""

from .init import get_session, init_database, verify_setup
from .models import AuditLog, Base, Chunk, Document, Embedding, Source

__all__ = [
    "Base",
    "Source",
    "Document",
    "Chunk",
    "Embedding",
    "AuditLog",
    "init_database",
    "verify_setup",
    "get_session",
]
