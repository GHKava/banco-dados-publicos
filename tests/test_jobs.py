"""
Tests for Redis and RQ setup.
"""


def test_redis_import():
    """Test redis package can be imported."""
    import redis

    assert redis is not None


def test_rq_import():
    """Test rq package can be imported."""
    import rq

    assert rq is not None


def test_job_queue_creation():
    """Test JobQueue can be instantiated."""
    from src.jobs import JobQueue

    queue = JobQueue(redis_url="redis://localhost:6379/0", queue_name="test")
    assert queue.queue_name == "test"


def test_example_job():
    """Test example job function."""
    from src.jobs.tasks import example_job

    result = example_job(5, 3)
    assert result == 8


def test_fetch_source_task():
    """Test fetch source task."""
    from src.jobs.tasks import fetch_source_task

    result = fetch_source_task("SRC-001")
    assert result["source_id"] == "SRC-001"
    assert result["status"] == "success"


def test_process_document_task():
    """Test process document task."""
    from src.jobs.tasks import process_document_task

    result = process_document_task("doc-123")
    assert result["doc_id"] == "doc-123"
    assert result["status"] == "cleaned"
