"""
Tests for database schema and models.
"""


def test_database_imports():
    """Test that database modules can be imported."""
    from src.database import AuditLog, Base, Chunk, Document, Embedding, Source

    assert Base is not None
    assert Source is not None
    assert Document is not None
    assert Chunk is not None
    assert Embedding is not None
    assert AuditLog is not None


def test_database_init_imports():
    """Test that database init functions can be imported."""
    from src.database import get_session, init_database, verify_setup

    assert init_database is not None
    assert verify_setup is not None
    assert get_session is not None


def test_source_model_attributes():
    """Test Source model has expected attributes."""
    from src.database import Source

    # Check key columns exist
    assert hasattr(Source, "source_id")
    assert hasattr(Source, "name")
    assert hasattr(Source, "license_status")
    assert hasattr(Source, "default_storage_mode")
    assert hasattr(Source, "pii_expected")


def test_document_model_attributes():
    """Test Document model has expected attributes."""
    from src.database import Document

    assert hasattr(Document, "doc_id")
    assert hasattr(Document, "source_id")
    assert hasattr(Document, "url")
    assert hasattr(Document, "url_hash")
    assert hasattr(Document, "content_hash")
    assert hasattr(Document, "status")
    assert hasattr(Document, "has_pii")


def test_chunk_model_attributes():
    """Test Chunk model has expected attributes."""
    from src.database import Chunk

    assert hasattr(Chunk, "chunk_id")
    assert hasattr(Chunk, "doc_id")
    assert hasattr(Chunk, "chunk_hash")
    assert hasattr(Chunk, "content")
    assert hasattr(Chunk, "chunk_index")


def test_embedding_model_attributes():
    """Test Embedding model has expected attributes."""
    from src.database import Embedding

    assert hasattr(Embedding, "embedding_id")
    assert hasattr(Embedding, "chunk_id")
    assert hasattr(Embedding, "vector")
    assert hasattr(Embedding, "model_name")
    assert hasattr(Embedding, "content_hash")


def test_audit_log_model_attributes():
    """Test AuditLog model has expected attributes."""
    from src.database import AuditLog

    assert hasattr(AuditLog, "log_id")
    assert hasattr(AuditLog, "event_type")
    assert hasattr(AuditLog, "actor")
    assert hasattr(AuditLog, "action")
    assert hasattr(AuditLog, "result")
