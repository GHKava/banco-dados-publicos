"""
Audit logging for compliance tracking.

Provides structured logging of policy decisions, source updates, and fetch attempts.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

logger = logging.getLogger(__name__)


def _get_session():
    from src.database import get_session

    return get_session()


def _get_model():
    from src.database.models import AuditLog

    return AuditLog


def _get_sqlalchemy() -> Tuple[Any, Any]:
    from sqlalchemy import func, select

    return func, select


def log_event(
    event_type: str,
    source_id: Optional[str] = None,
    action: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    actor: Optional[str] = None,
    doc_id: Optional[UUID] = None,
    result: Optional[str] = "success",
    error_message: Optional[str] = None,
    run_id: Optional[UUID] = None,
    job_id: Optional[UUID] = None,
) -> UUID:
    """
    Log an audit event.

    Args:
        event_type: Type of event
        source_id: Source ID (optional)
        action: Action performed (optional)
        details: Additional metadata (optional)
        actor: User/agent ID (optional)
        doc_id: Document UUID (optional)
        result: Result status (default: 'success')

    Returns:
        UUID of created audit log entry
    """
    session = _get_session()
    try:
        AuditLog = _get_model()
        audit_entry = AuditLog(
            event_type=event_type,
            event_timestamp=datetime.utcnow(),
            source_id=source_id,
            doc_id=doc_id,
            actor=actor,
            action=action,
            details=details,
            result=result,
            error_message=error_message,
            run_id=run_id,
            job_id=job_id,
        )
        session.add(audit_entry)
        session.commit()
        session.refresh(audit_entry)
        return audit_entry.log_id
    except Exception as exc:  # pragma: no cover - DB failure path
        session.rollback()
        logger.exception("Audit log failed: %s", exc)
        raise
    finally:
        session.close()


def query_audit_log(
    event_type: Optional[str] = None,
    source_id: Optional[str] = None,
    actor: Optional[str] = None,
    limit: int = 100,
) -> List[AuditLog]:
    """
    Query audit logs with optional filters.

    Args:
        event_type: Filter by event type
        source_id: Filter by source ID
        actor: Filter by actor
        limit: Maximum results (default: 100)

    Returns:
        List of AuditLog objects ordered by timestamp DESC
    """
    session = _get_session()
    try:
        AuditLog = _get_model()
        func, select = _get_sqlalchemy()
        stmt = select(AuditLog).order_by(AuditLog.event_timestamp.desc()).limit(limit)

        if event_type:
            stmt = stmt.where(AuditLog.event_type == event_type)
        if source_id:
            stmt = stmt.where(AuditLog.source_id == source_id)
        if actor:
            stmt = stmt.where(AuditLog.actor == actor)

        return list(session.execute(stmt).scalars().all())
    finally:
        session.close()


def get_audit_stats() -> Dict[str, Any]:
    """
    Get summary statistics of audit logs.

    Returns:
        dict with total_events, events_by_type, latest_timestamp
    """
    session = _get_session()
    try:
        AuditLog = _get_model()
        func, select = _get_sqlalchemy()
        total = session.execute(select(func.count(AuditLog.log_id))).scalar()
        events_by_type_query = select(AuditLog.event_type, func.count(AuditLog.log_id)).group_by(
            AuditLog.event_type
        )
        events_by_type = {row[0]: row[1] for row in session.execute(events_by_type_query)}
        latest_ts = session.execute(select(func.max(AuditLog.event_timestamp))).scalar()

        return {
            "total_events": total or 0,
            "events_by_type": events_by_type,
            "latest_timestamp": latest_ts,
        }
    finally:
        session.close()
