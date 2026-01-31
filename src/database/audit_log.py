"""
Audit logging for compliance tracking.

Uses existing AuditLog model from models.py.
"""

from typing import Any, Dict, List, Optional
from uuid import UUID

from sqlalchemy import func, select

from src.database.database import get_session
from src.database.models import AuditLog


def log_event(
    event_type: str,
    source_id: Optional[str] = None,
    action: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    actor: Optional[str] = None,
    doc_id: Optional[UUID] = None,
    result: Optional[str] = "success",
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
    with get_session() as session:
        audit_entry = AuditLog(
            event_type=event_type,
            source_id=source_id,
            action=action,
            details=details or {},
            actor=actor,
            doc_id=doc_id,
            result=result,
        )
        session.add(audit_entry)
        session.commit()
        return audit_entry.log_id


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
    with get_session() as session:
        stmt = select(AuditLog).order_by(AuditLog.event_timestamp.desc()).limit(limit)

        if event_type:
            stmt = stmt.where(AuditLog.event_type == event_type)
        if source_id:
            stmt = stmt.where(AuditLog.source_id == source_id)
        if actor:
            stmt = stmt.where(AuditLog.actor == actor)

        return list(session.execute(stmt).scalars().all())


def get_audit_stats() -> Dict[str, Any]:
    """
    Get summary statistics of audit logs.

    Returns:
        dict with total_events, events_by_type, latest_timestamp
    """
    with get_session() as session:
        # Total events
        total = session.execute(select(func.count(AuditLog.log_id))).scalar()

        # Events by type
        events_by_type_query = select(AuditLog.event_type, func.count(AuditLog.log_id)).group_by(AuditLog.event_type)
        events_by_type = {row[0]: row[1] for row in session.execute(events_by_type_query)}

        # Latest timestamp
        latest_ts = session.execute(select(func.max(AuditLog.event_timestamp))).scalar()

        return {
            "total_events": total or 0,
            "events_by_type": events_by_type,
            "latest_timestamp": latest_ts,
        }
