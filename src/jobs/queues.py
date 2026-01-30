"""RQ queue definitions."""

from rq import Queue

from src.jobs.redis_client import get_redis_connection


def get_queue(name: str = "default") -> Queue:
    """
    Get RQ queue by name.

    Args:
        name: Queue name ('default', 'high', 'low')

    Returns:
        Queue: RQ queue instance

    Example:
        >>> queue = get_queue('default')
        >>> job = queue.enqueue(my_function, arg1, arg2)
    """
    redis_conn = get_redis_connection()
    return Queue(name, connection=redis_conn)


# Pre-defined queues
default_queue = get_queue("default")
high_queue = get_queue("high")
low_queue = get_queue("low")
