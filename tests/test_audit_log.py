"""
Tests for audit_log helpers (no DB connection required).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List

from src.database import audit_log


class DummyColumn:
    def __init__(self, name: str):
        self.name = name

    def desc(self):
        return ("desc", self.name)


class DummyAuditLog:
    event_timestamp = DummyColumn("event_timestamp")
    event_type = DummyColumn("event_type")
    source_id = DummyColumn("source_id")
    actor = DummyColumn("actor")
    log_id = DummyColumn("log_id")

    def __init__(self, **kwargs):
        self.event_type_value = kwargs.get("event_type")
        self.source_id_value = kwargs.get("source_id")
        self.actor_value = kwargs.get("actor")
        self.action_value = kwargs.get("action")
        self.details_value = kwargs.get("details")
        self.result_value = kwargs.get("result")
        self.log_id = "dummy-log-id"


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


def _patch_sqlalchemy(monkeypatch):
    class DummyQuery:
        def order_by(self, _arg):
            return self

        def limit(self, _arg):
            return self

        def where(self, _arg):
            return self

        def group_by(self, _arg):
            return self

    class DummyFunc:
        @staticmethod
        def count(arg):
            return ("count", arg)

        @staticmethod
        def max(arg):
            return ("max", arg)

    def dummy_select(*args, **kwargs):
        return DummyQuery()

    monkeypatch.setattr(audit_log, "_get_sqlalchemy", lambda: (DummyFunc, dummy_select))


def test_log_event_creates_entry(monkeypatch):
    session = DummySession()
    monkeypatch.setattr(audit_log, "_get_session", lambda: session)
    monkeypatch.setattr(audit_log, "_get_model", lambda: DummyAuditLog)
    _patch_sqlalchemy(monkeypatch)

    log_id = audit_log.log_event(event_type="policy_check", source_id="SRC-001")

    assert log_id is not None
    assert session.add_called is True
    assert session.commit_called is True
    assert session.refresh_called is True
    assert session.closed is True


def test_query_audit_log_returns_list(monkeypatch):
    expected = [DummyAuditLog(event_type="policy_check")]
    session = DummySession(execute_results=[DummyExecute(scalars_list=expected)])
    monkeypatch.setattr(audit_log, "_get_session", lambda: session)
    monkeypatch.setattr(audit_log, "_get_model", lambda: DummyAuditLog)
    _patch_sqlalchemy(monkeypatch)

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
    monkeypatch.setattr(audit_log, "_get_session", lambda: session)
    monkeypatch.setattr(audit_log, "_get_model", lambda: DummyAuditLog)
    _patch_sqlalchemy(monkeypatch)

    stats = audit_log.get_audit_stats()

    assert stats["total_events"] == 5
    assert stats["events_by_type"]["policy_check"] == 3
    assert stats["events_by_type"]["source_update"] == 2
    assert stats["latest_timestamp"] == "2026-01-31T02:30:00Z"
    assert session.closed is True
