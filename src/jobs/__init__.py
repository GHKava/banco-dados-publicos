"""
Job queue module for banco-dados-publicos.

Uses Redis + RQ for async job processing.
"""

import logging
from typing import Any, Callable, Optional

from redis import Redis
from rq import Queue, Worker
from rq.job import JobStatus

logger = logging.getLogger(__name__)


class JobQueue:
    """Wrapper for Redis Queue operations."""

    def __init__(self, redis_url: str = "redis://localhost:6379/0", queue_name: str = "default"):
        """
        Initialize job queue.

        Args:
            redis_url: Redis connection URL
            queue_name: Queue name (default or by job type)
        """
        self.redis = Redis.from_url(redis_url, decode_responses=True)
        self.queue = Queue(queue_name, connection=self.redis)
        self.queue_name = queue_name

    def enqueue(
        self,
        func: Callable,
        *args,
        job_id: Optional[str] = None,
        **kwargs,
    ) -> str:
        """
        Enqueue a job.

        Args:
            func: Callable to execute
            args: Positional arguments
            job_id: Optional job ID for idempotency
            kwargs: Keyword arguments

        Returns:
            Job ID
        """
        job = self.queue.enqueue(func, *args, job_id=job_id, **kwargs)
        logger.info(f"Job enqueued: {job.id} in queue '{self.queue_name}'")
        return str(job.id)

    def get_job_status(self, job_id: str) -> str:
        """Get job status."""
        job = self.queue.fetch_job(job_id)
        if not job:
            return "not_found"
        status = job.get_status()
        return str(status) if status else "unknown"

    def get_job_result(self, job_id: str) -> Any:
        """Get job result (if complete)."""
        job = self.queue.fetch_job(job_id)
        if not job:
            return None
        if job.get_status() == JobStatus.FINISHED:
            return job.result
        return None

    def delete_job(self, job_id: str) -> bool:
        """Delete a job."""
        job = self.queue.fetch_job(job_id)
        if job:
            job.delete()
            logger.info(f"Job deleted: {job_id}")
            return True
        return False

    def get_worker(self) -> Worker:
        """Get worker for this queue."""
        return Worker([self.queue], connection=self.redis)

    def test_connection(self) -> bool:
        """Test Redis connectivity."""
        try:
            self.redis.ping()
            logger.info(f"✅ Redis connection OK (queue: {self.queue_name})")
            return True
        except Exception as e:
            logger.error(f"❌ Redis connection failed: {e}")
            return False


def get_job_queue(redis_url: Optional[str] = None, queue_name: str = "default") -> JobQueue:
    """
    Factory for JobQueue.

    Args:
        redis_url: Redis connection URL (from env if None)
        queue_name: Queue name

    Returns:
        JobQueue instance
    """
    import os

    if not redis_url:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    if redis_url is None:
        redis_url = "redis://localhost:6379/0"

    return JobQueue(redis_url, queue_name)
