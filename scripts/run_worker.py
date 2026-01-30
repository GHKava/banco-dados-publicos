"""RQ worker runner script."""

import argparse
import logging
import sys

from rq import Worker

from src.jobs.redis_client import get_redis_connection

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def main():
    """Run RQ worker."""
    parser = argparse.ArgumentParser(description="RQ Worker")
    parser.add_argument("--queue", default="default", help="Queue name (default, high, low)")
    parser.add_argument("--burst", action="store_true", help="Run until queue empty, then exit")

    args = parser.parse_args()

    try:
        redis_conn = get_redis_connection()

        # Test connection
        if not redis_conn.ping():
            logger.error("Cannot connect to Redis")
            sys.exit(1)

        logger.info(f"Starting worker for queue '{args.queue}' (burst={args.burst})")

        worker = Worker([args.queue], connection=redis_conn)
        worker.work(burst=args.burst)

    except KeyboardInterrupt:
        logger.info("Worker interrupted by user")
    except Exception as e:
        logger.exception(f"Worker error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
