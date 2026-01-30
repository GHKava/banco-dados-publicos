"""
Source registry bot - CRUD operations for data sources with policy enforcement.
"""

import logging
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.bots.validators import validate_source_policy
from src.database.models import Source

logger = logging.getLogger(__name__)


class SourceRegistryBot:
    """Bot for managing source registry with policy compliance."""

    def __init__(self, session: Session):
        """Initialize bot with database session."""
        self.session = session

    def list_sources(self, compliance_only: bool = False) -> list[dict]:
        """List all sources."""
        stmt = select(Source)
        sources = self.session.execute(stmt).scalars().all()

        result = []
        for src in sources:
            src_dict = {
                "source_id": src.source_id,
                "name": src.name,
                "base_url": src.base_url,
                "policy": src.metadata_.get("policy_level", "UNKNOWN"),
                "status": "active" if src.is_active else "inactive",
            }

            if compliance_only:
                is_compliant, msg = validate_source_policy(src)
                src_dict["compliant"] = is_compliant
                src_dict["compliance_msg"] = msg

            result.append(src_dict)

        return result

    def get_source(self, source_id: str) -> Optional[dict]:
        """Get source by ID."""
        stmt = select(Source).where(Source.source_id == source_id)
        src = self.session.execute(stmt).scalar_one_or_none()

        if not src:
            return None

        return {
            "source_id": src.source_id,
            "name": src.name,
            "base_url": src.base_url,
            "metadata": src.metadata_,
            "created_at": src.created_at,
            "updated_at": src.updated_at,
        }

    def add_source(self, source_id: str, name: str, base_url: str, metadata: dict) -> dict:
        """Register new source with policy check."""
        # Validate policy
        is_compliant, msg = validate_source_policy(
            {"source_id": source_id, "name": name, "base_url": base_url, "metadata": metadata}
        )
        if not is_compliant:
            logger.warning(f"Source {source_id} failed policy check: {msg}")
            raise ValueError(f"Policy check failed: {msg}")

        # Create source
        src = Source(
            source_id=source_id,
            name=name,
            base_url=base_url,
            metadata_=metadata,
            is_active=True,
        )
        self.session.add(src)
        self.session.commit()

        logger.info(f"Source registered: {source_id}")
        return self.get_source(source_id) or {}

    def update_source(
        self,
        source_id: str,
        name: Optional[str] = None,
        base_url: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Update source metadata."""
        stmt = select(Source).where(Source.source_id == source_id)
        src = self.session.execute(stmt).scalar_one_or_none()

        if not src:
            raise ValueError(f"Source not found: {source_id}")

        if name:
            src.name = name
        if base_url:
            src.base_url = base_url
        if metadata:
            src.metadata_ = metadata

        self.session.commit()
        logger.info(f"Source updated: {source_id}")
        return self.get_source(source_id) or {}

    def remove_source(self, source_id: str) -> bool:
        """Soft-delete source (mark inactive)."""
        stmt = select(Source).where(Source.source_id == source_id)
        src = self.session.execute(stmt).scalar_one_or_none()

        if not src:
            return False

        src.is_active = False
        self.session.commit()

        logger.info(f"Source deactivated: {source_id}")
        return True

    def validate_source(self, source_id: str) -> tuple[bool, str]:
        """Check source compliance with policy."""
        stmt = select(Source).where(Source.source_id == source_id)
        src = self.session.execute(stmt).scalar_one_or_none()

        if not src:
            return False, f"Source not found: {source_id}"

        return validate_source_policy(src)
