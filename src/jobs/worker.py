"""
RQ Worker runner.

Usage:
    python -m src.jobs.worker
    python -m src.jobs.worker --burst  (run until queue empty, then exit)
"""

import logging
import os

from src.jobs import get_job_queue

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_worker(queue_name: str = "default", burst: bool = False) -> None:
    """
    Run RQ worker.

    Args:
        queue_name: Queue to listen on
        burst: If True, exit when queue is empty
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    job_queue = get_job_queue(redis_url, queue_name)

    # Test connection
    if not job_queue.test_connection():
        logger.error("Cannot connect to Redis")
        return

    # Get worker and start
    worker = job_queue.get_worker()
    logger.info(f"Worker starting (burst={burst})")

    try:
        worker.work(burst=burst)
    except KeyboardInterrupt:
        logger.info("Worker interrupted by user")
    except Exception as e:
        logger.exception(f"Worker error: {e}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="RQ Worker")
    parser.add_argument("--burst", action="store_true", help="Exit when queue empty")
    parser.add_argument("--queue", default="default", help="Queue name")

    args = parser.parse_args()

    run_worker(queue_name=args.queue, burst=args.burst)
