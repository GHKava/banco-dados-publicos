"""Redis connection pool for RQ."""

import os

import redis
from redis import ConnectionPool

# Redis URL from environment
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_redis_connection() -> redis.Redis:
    """
    Get Redis connection from pool.

    Returns:
        redis.Redis: Redis client instance

    Example:
        >>> r = get_redis_connection()
        >>> r.ping()
        True
    """
    pool = ConnectionPool.from_url(REDIS_URL, decode_responses=True, max_connections=10)
    return redis.Redis(connection_pool=pool)
