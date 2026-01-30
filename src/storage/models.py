"""
SQLAlchemy ORM models for metadata storage.

Schema v0 — MVP baseline:
- sources: Source metadata (allowlist, robots, ToS, license)
- documents: Fetched documents with metadata
- chunks: Text chunks for embeddings
- embeddings: Vector representations (TEXT format for MVP, pgvector in T-015)
- audit_log: Compliance tracking for all CRUD operations
"""

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from sqlalchemy import BigInteger, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class Source(Base):
    """
    Source registry table (allowlist).

    Tracks compliance status, robots.txt policy, ToS acceptance, and license info.
    """

    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)
    base_url: Mapped[str] = mapped_column(String(512), nullable=False)
    source_type: Mapped[str] = mapped_column(
        Enum("government", "academic", "news", "other", name="source_type_enum"),
        nullable=False,
        index=True,
    )
    license_info: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    robots_policy: Mapped[str] = mapped_column(
        Enum("ALLOW", "BLOCK", "METADATA_ONLY", name="robots_policy_enum"),
        nullable=False,
        default="METADATA_ONLY",
        index=True,
    )
    tos_compliance: Mapped[bool] = mapped_column(default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("ACTIVE", "INACTIVE", "PENDING_REVIEW", name="source_status_enum"),
        nullable=False,
        default="PENDING_REVIEW",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    documents: Mapped[list["Document"]] = relationship(
        "Document", back_populates="source", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Source(id={self.id}, name={self.name}, status={self.status})>"


class Document(Base):
    """
    Document metadata table.

    Stores fetched documents with URL, hash, fetch timestamp, and compliance status.
    """

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    source_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("sources.id", ondelete="CASCADE"), nullable=False, index=True
    )
    url: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    content_hash: Mapped[Optional[str]] = mapped_column(String(64), nullable=True, index=True)
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)  # renamed from "metadata" (reserved)
    fetch_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status: Mapped[str] = mapped_column(
        Enum("PENDING", "PROCESSED", "ERROR", "BLOCKED", name="document_status_enum"),
        nullable=False,
        default="PENDING",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    source: Mapped["Source"] = relationship("Source", back_populates="documents")
    chunks: Mapped[list["Chunk"]] = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")

    __table_args__ = (Index("idx_documents_source_status", "source_id", "status"),)

    def __repr__(self) -> str:
        return f"<Document(id={self.id}, url={self.url[:50]}, status={self.status})>"


class Chunk(Base):
    """
    Text chunk table for embeddings.

    Splits documents into chunks for vector search (chunk_index for ordering).
    """

    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    document_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    meta: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)  # renamed from "metadata" (reserved)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    document: Mapped["Document"] = relationship("Document", back_populates="chunks")
    embeddings: Mapped[list["Embedding"]] = relationship(
        "Embedding", back_populates="chunk", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("idx_chunks_document_index", "document_id", "chunk_index", unique=True),)

    def __repr__(self) -> str:
        return f"<Chunk(id={self.id}, document_id={self.document_id}, index={self.chunk_index})>"


class Embedding(Base):
    """
    Embedding table (vector storage).

    NOTE: Using TEXT for MVP (JSON array format: "[0.123, 0.456, ...]").
    pgvector extension will be added in T-015 (semantic search) via migration:
    ALTER COLUMN vector TYPE vector(384) USING vector::vector(384);
    """

    __tablename__ = "embeddings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    chunk_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("chunks.id", ondelete="CASCADE"), nullable=False, index=True
    )
    model_name: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    vector: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # JSON array format: "[0.123, 0.456, ...]" (pgvector in T-015)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    chunk: Mapped["Chunk"] = relationship("Chunk", back_populates="embeddings")

    __table_args__ = (Index("idx_embeddings_chunk_model", "chunk_id", "model_name", unique=True),)

    def __repr__(self) -> str:
        return f"<Embedding(id={self.id}, chunk_id={self.chunk_id}, model={self.model_name})>"


class Audit_log(Base):
    """
    Audit log table for compliance tracking.

    Records all CRUD operations on sources, documents, chunks, embeddings.
    """

    __tablename__ = "audit_log"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(
        Enum("source", "document", "chunk", "embedding", name="entity_type_enum"),
        nullable=False,
        index=True,
    )
    entity_id: Mapped[int] = mapped_column(BigInteger, nullable=False, index=True)
    action: Mapped[str] = mapped_column(
        Enum("CREATE", "UPDATE", "DELETE", name="action_enum"),
        nullable=False,
        index=True,
    )
    old_value: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    new_value: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB, nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    __table_args__ = (Index("idx_audit_entity", "entity_type", "entity_id"),)

    def __repr__(self) -> str:
        return f"<Audit_log(id={self.id}, entity={self.entity_type}/{self.entity_id}, action={self.action})>"
