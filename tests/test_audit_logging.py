"""
Tests for audit logging module.
"""

from uuid import uuid4

from src.database.audit_log import get_audit_stats, log_event, query_audit_log


class TestLogEvent:
    """Tests for log_event function"""

    def test_log_event_minimal(self):
        """Test logging event with minimal params"""
        log_id = log_event(event_type="test_event")

        assert log_id is not None
        assert isinstance(log_id, type(uuid4()))

    def test_log_event_full(self):
        """Test logging event with all params"""
        log_id = log_event(
            event_type="policy_check",
            source_id="SRC-TEST",
            action="check_robots",
            details={"decision": "ALLOW", "reason": "No robots.txt"},
            actor="ORQ",
            result="success",
        )

        assert log_id is not None

    def test_log_event_with_doc_id(self):
        """Test logging event with document UUID"""
        doc_id = uuid4()

        log_id = log_event(
            event_type="fetch_attempt",
            source_id="SRC-001",
            action="fetch",
            doc_id=doc_id,
            actor="FetchBot",
        )

        assert log_id is not None


class TestQueryAuditLog:
    """Tests for query_audit_log function"""

    def test_query_audit_log_no_filters(self):
        """Test querying logs without filters"""
        # Log some events
        log_event(event_type="test1", source_id="SRC-001")
        log_event(event_type="test2", source_id="SRC-002")

        logs = query_audit_log()

        assert len(logs) >= 2
        assert logs[0].event_timestamp > logs[-1].event_timestamp  # DESC order

    def test_query_audit_log_by_event_type(self):
        """Test filtering by event type"""
        log_event(event_type="test_filter", source_id="SRC-001")

        logs = query_audit_log(event_type="test_filter")

        assert len(logs) >= 1
        assert all(log.event_type == "test_filter" for log in logs)

    def test_query_audit_log_by_source(self):
        """Test filtering by source ID"""
        log_event(event_type="test", source_id="SRC-FILTER-TEST")

        logs = query_audit_log(source_id="SRC-FILTER-TEST")

        assert len(logs) >= 1
        assert all(log.source_id == "SRC-FILTER-TEST" for log in logs)

    def test_query_audit_log_by_actor(self):
        """Test filtering by actor"""
        log_event(event_type="test", actor="TestActor")

        logs = query_audit_log(actor="TestActor")

        assert len(logs) >= 1
        assert all(log.actor == "TestActor" for log in logs)

    def test_query_audit_log_limit(self):
        """Test limit parameter"""
        # Log multiple events
        for i in range(15):
            log_event(event_type=f"test_{i}")

        logs = query_audit_log(limit=5)

        assert len(logs) <= 5


class TestGetAuditStats:
    """Tests for get_audit_stats function"""

    def test_get_audit_stats(self):
        """Test getting audit statistics"""
        # Log some events
        log_event(event_type="stats_test_1")
        log_event(event_type="stats_test_1")
        log_event(event_type="stats_test_2")

        stats = get_audit_stats()

        assert "total_events" in stats
        assert "events_by_type" in stats
        assert "latest_timestamp" in stats
        assert stats["total_events"] >= 3
        assert isinstance(stats["events_by_type"], dict)

    def test_get_audit_stats_empty(self):
        """Test stats when no logs exist (initial state)"""
        stats = get_audit_stats()

        assert stats["total_events"] >= 0
        assert isinstance(stats["events_by_type"], dict)
