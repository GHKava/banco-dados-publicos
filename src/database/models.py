"""
Database models for Banco de Dados Interrelacional.

SQLAlchemy ORM models matching schema.sql.
"""

from datetime import datetime
from uuid import uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY, Boolean, Column, Date, DateTime, Decimal, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Source(Base):
    """Data source registry with crawl and compliance policies."""

    __tablename__ = "sources"

    source_id = Column(String(50), primary_key=True)
    name = Column(String(255), nullable=False)
    owner_org = Column(String(255))
    base_domains = Column(ARRAY(Text))
    entrypoints = Column(ARRAY(Text))

    # Crawl policy
    robots_respect = Column(Boolean, default=True)
    user_agent = Column(String(255))
    rate_limit_rps = Column(Decimal(5, 2), default=0.2)
    concurrency = Column(Integer, default=1)
    allow_paths = Column(ARRAY(Text))
    deny_paths = Column(ARRAY(Text))

    # License & compliance
    license_status = Column(String(50), default="unknown")
    license_evidence = Column(Text)
    default_storage_mode = Column(String(50), default="METADATA_ONLY")

    # Data handling (LGPD)
    pii_expected = Column(String(20), default="low")
    pii_actions = Column(ARRAY(Text))
    retention_days = Column(Integer, default=365)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    notes = Column(Text)

    # Relationships
    documents = relationship("Document", back_populates="source", cascade="all, delete-orphan")


class Document(Base):
    """Collected and processed documents."""

    __tablename__ = "documents"

    doc_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    source_id = Column(String(50), ForeignKey("sources.source_id", ondelete="CASCADE"), nullable=False)

    # URL & Identity
    url = Column(Text, nullable=False)
    url_canonical = Column(Text)
    url_hash = Column(String(64), unique=True, nullable=False)

    # Content identity
    content_hash = Column(String(64))
    content_type = Column(String(100))

    # Fetch metadata
    fetched_at = Column(DateTime)
    http_status = Column(Integer)
    http_headers = Column(JSONB)

    # Processing status
    status = Column(String(50), default="raw")
    processing_errors = Column(JSONB)

    # Content
    title = Column(Text)
    author = Column(Text)
    published_date = Column(Date)
    language = Column(String(10), default="pt")

    raw_content = Column(Text)
    clean_content = Column(Text)
    content_length = Column(Integer)

    # Quality & dedup
    quality_score = Column(Decimal(3, 2))
    is_duplicate = Column(Boolean, default=False)
    duplicate_of = Column(PGUUID(as_uuid=True), ForeignKey("documents.doc_id"))

    # Compliance & PII
    has_pii = Column(Boolean, default=False)
    pii_detected = Column(JSONB)

    # Enrichment
    entities = Column(JSONB)
    topics = Column(JSONB)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Versioning
    version = Column(Integer, default=1)
    previous_version_id = Column(PGUUID(as_uuid=True), ForeignKey("documents.doc_id"))

    # Relationships
    source = relationship("Source", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")


class Chunk(Base):
    """Text segments for RAG indexing."""

    __tablename__ = "chunks"

    chunk_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    doc_id = Column(PGUUID(as_uuid=True), ForeignKey("documents.doc_id", ondelete="CASCADE"), nullable=False)

    # Chunk identity
    chunk_hash = Column(String(64), unique=True, nullable=False)
    chunk_index = Column(Integer, nullable=False)

    # Content
    content = Column(Text, nullable=False)
    content_length = Column(Integer, nullable=False)

    # Position in document
    start_char = Column(Integer)
    end_char = Column(Integer)

    # Metadata inheritance
    title = Column(Text)
    published_date = Column(Date)
    source_id = Column(String(50))

    # Chunking metadata
    chunk_method = Column(String(50), default="fixed_size")
    overlap_tokens = Column(Integer, default=0)

    # Quality
    quality_score = Column(Decimal(3, 2))

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    document = relationship("Document", back_populates="chunks")
    embeddings = relationship("Embedding", back_populates="chunk", cascade="all, delete-orphan")


class Embedding(Base):
    """Vector embeddings for semantic search."""

    __tablename__ = "embeddings"

    embedding_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    chunk_id = Column(PGUUID(as_uuid=True), ForeignKey("chunks.chunk_id", ondelete="CASCADE"), nullable=False)

    # Vector
    vector = Column(Vector(384))

    # Model info
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50))

    # Cache key
    content_hash = Column(String(64), nullable=False)

    # Timestamp
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    chunk = relationship("Chunk", back_populates="embeddings")


class AuditLog(Base):
    """Audit log for compliance and traceability."""

    __tablename__ = "audit_log"

    log_id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Event
    event_type = Column(String(50), nullable=False)
    event_timestamp = Column(DateTime, default=datetime.utcnow)

    # Context
    source_id = Column(String(50))
    doc_id = Column(PGUUID(as_uuid=True))
    chunk_id = Column(PGUUID(as_uuid=True))

    # Actor
    actor = Column(String(100))

    # Action details
    action = Column(String(50))
    details = Column(JSONB)

    # Result
    result = Column(String(20))
    error_message = Column(Text)

    # Metadata
    run_id = Column(PGUUID(as_uuid=True))
    job_id = Column(PGUUID(as_uuid=True))
