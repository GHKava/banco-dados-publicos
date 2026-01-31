"""
Database package for Banco de Dados Interrelacional.

Uses lazy imports to avoid loading SQLAlchemy on module import.
"""

from __future__ import annotations

import importlib
from typing import Any

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


def __getattr__(name: str) -> Any:
    if name in {"get_session", "init_database", "verify_setup"}:
        module = importlib.import_module("src.database.init")
        return getattr(module, name)
    if name in {"Base", "Source", "Document", "Chunk", "Embedding", "AuditLog"}:
        module = importlib.import_module("src.database.models")
        return getattr(module, name)
    raise AttributeError(f"module 'src.database' has no attribute {name}")
