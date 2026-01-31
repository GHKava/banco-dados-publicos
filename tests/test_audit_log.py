"""
Tests for audit_log helpers (no DB connection required).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List

from src.database import audit_log


@dataclass
class DummyExecute:
    scalar_value: Any = None
    scalars_list: List[Any] | None = None
    rows: List[tuple] | None = None

    def scalar(self):
        return self.scalar_value

    def scalars(self):
        return self

    def all(self):
        return self.scalars_list or []

    def __iter__(self) -> Iterable:
        return iter(self.rows or [])


class DummySession:
    def __init__(self, execute_results: list[DummyExecute] | None = None):
        self.execute_results = execute_results or []
        self.add_called = False
        self.commit_called = False
        self.refresh_called = False
        self.rollback_called = False
        self.closed = False

    def add(self, _obj):
        self.add_called = True

    def commit(self):
        self.commit_called = True

    def refresh(self, _obj):
        self.refresh_called = True

    def rollback(self):
        self.rollback_called = True

    def close(self):
        self.closed = True

    def execute(self, _stmt):
        if not self.execute_results:
            return DummyExecute()
        return self.execute_results.pop(0)


def test_log_event_creates_entry(monkeypatch):
    session = DummySession()
    monkeypatch.setattr(audit_log, "get_session", lambda: session)

    log_id = audit_log.log_event(event_type="policy_check", source_id="SRC-001")

    assert log_id is not None
    assert session.add_called is True
    assert session.commit_called is True
    assert session.refresh_called is True
    assert session.closed is True


def test_query_audit_log_returns_list(monkeypatch):
    expected = [audit_log.AuditLog(event_type="policy_check")]
    session = DummySession(execute_results=[DummyExecute(scalars_list=expected)])
    monkeypatch.setattr(audit_log, "get_session", lambda: session)

    result = audit_log.query_audit_log(event_type="policy_check", limit=1)

    assert result == expected
    assert session.closed is True


def test_get_audit_stats(monkeypatch):
    session = DummySession(
        execute_results=[
            DummyExecute(scalar_value=5),
            DummyExecute(rows=[("policy_check", 3), ("source_update", 2)]),
            DummyExecute(scalar_value="2026-01-31T02:30:00Z"),
        ]
    )
    monkeypatch.setattr(audit_log, "get_session", lambda: session)

    stats = audit_log.get_audit_stats()

    assert stats["total_events"] == 5
    assert stats["events_by_type"]["policy_check"] == 3
    assert stats["events_by_type"]["source_update"] == 2
    assert stats["latest_timestamp"] == "2026-01-31T02:30:00Z"
    assert session.closed is True
