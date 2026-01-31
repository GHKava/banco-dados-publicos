"""
URL Frontier - Priority queue for URL crawling.

Redis-backed priority queue with deduplication and source tracking.
"""

import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, urlunparse

import redis


@dataclass
class FrontierURL:
    """URL with metadata for frontier queue."""

    url: str
    source_id: str
    priority: int
    added_timestamp: float


class URLFrontier:
    """
    URL frontier (priority queue) for managing crawl URLs.

    Uses Redis sorted set for priority queue and set for deduplication.
    """

    def __init__(self, redis_client: redis.Redis, ttl_days: int = 30):
        """
        Initialize URL frontier.

        Args:
            redis_client: Redis connection
            ttl_days: TTL for seen URLs (default: 30 days)
        """
        self.redis = redis_client
        self.ttl_seconds = ttl_days * 86400

        # Redis keys
        self.pending_key = "frontier:urls:pending"
        self.seen_key = "frontier:urls:seen"
        self.stats_prefix = "frontier:stats"

    def _canonicalize_url(self, url: str) -> str:
        """
        Canonicalize URL for deduplication.

        Args:
            url: Raw URL

        Returns:
            Canonicalized URL (lowercase scheme/netloc, sorted query params)
        """
        parsed = urlparse(url)

        # Normalize: lowercase scheme and netloc
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()

        # Remove default ports
        if (scheme == "http" and netloc.endswith(":80")) or (
            scheme == "https" and netloc.endswith(":443")
        ):
            netloc = netloc.rsplit(":", 1)[0]

        # Reconstruct (path, params, query, fragment preserved)
        canonical = urlunparse(
            (scheme, netloc, parsed.path, parsed.params, parsed.query, parsed.fragment)
        )

        return canonical

    def _compute_score(self, priority: int, timestamp: float) -> float:
        """
        Compute Redis sorted set score.

        Higher score = higher priority.
        Formula: priority * 1000 + (current_time - added_time)

        Args:
            priority: Priority (0-100)
            timestamp: Added timestamp (Unix seconds)

        Returns:
            Float score for sorted set
        """
        current_time = time.time()
        age_offset = current_time - timestamp
        return float(priority * 1000 + age_offset)

    def add_url(
        self, url: str, source_id: str, priority: int = 50, metadata: Optional[dict] = None
    ) -> bool:
        """
        Add URL to frontier.

        Args:
            url: URL to add
            source_id: Source ID (e.g., 'SRC-001')
            priority: Priority 0-100 (default: 50)
            metadata: Optional metadata (not stored in MVP)

        Returns:
            True if added, False if already seen
        """
        canonical_url = self._canonicalize_url(url)

        # Check if already seen
        if self.redis.sismember(self.seen_key, canonical_url):
            return False

        # Add to seen set with TTL
        self.redis.sadd(self.seen_key, canonical_url)
        self.redis.expire(self.seen_key, self.ttl_seconds)

        # Add to pending queue
        timestamp = time.time()
        score = self._compute_score(priority, timestamp)

        # Store URL with source_id as value (format: "source_id|url")
        value = f"{source_id}|{canonical_url}"
        self.redis.zadd(self.pending_key, {value: score})

        # Update stats
        stats_key = f"{self.stats_prefix}:{source_id}"
        self.redis.hincrby(stats_key, "added", 1)
        self.redis.expire(stats_key, self.ttl_seconds)

        return True

    def get_next_url(self) -> Optional[FrontierURL]:
        """
        Pop next URL from frontier (highest priority).

        Returns:
            FrontierURL or None if queue empty
        """
        # Pop highest score (ZREVRANGE returns highest first)
        result = self.redis.zpopmax(self.pending_key, count=1)

        if not result:
            return None

        value, score = result[0]
        value_str = value.decode("utf-8") if isinstance(value, bytes) else value

        # Parse "source_id|url"
        source_id, url = value_str.split("|", 1)

        # Reverse-engineer priority (approximate)
        priority = int(score / 1000)
        added_timestamp = time.time() - (score - priority * 1000)

        # Update stats
        stats_key = f"{self.stats_prefix}:{source_id}"
        self.redis.hincrby(stats_key, "crawled", 1)

        return FrontierURL(
            url=url, source_id=source_id, priority=priority, added_timestamp=added_timestamp
        )

    def get_queue_size(self) -> int:
        """
        Get total URLs in pending queue.

        Returns:
            Number of pending URLs
        """
        return self.redis.zcard(self.pending_key)

    def get_seen_count(self) -> int:
        """
        Get total unique URLs seen (ever added).

        Returns:
            Number of URLs in seen set
        """
        return self.redis.scard(self.seen_key)

    def get_stats(self) -> dict:
        """
        Get frontier statistics.

        Returns:
            dict with:
                - pending: int (URLs in queue)
                - seen: int (unique URLs seen)
                - by_source: dict (source_id → {added, crawled})
        """
        pending = self.get_queue_size()
        seen = self.get_seen_count()

        # Aggregate stats by source
        by_source = {}
        for key in self.redis.scan_iter(match=f"{self.stats_prefix}:*"):
            source_id = (
                key.decode("utf-8").split(":")[-1] if isinstance(key, bytes) else key.split(":")[-1]
            )
            stats = self.redis.hgetall(key)
            by_source[source_id] = {
                "added": int(stats.get(b"added", 0)),
                "crawled": int(stats.get(b"crawled", 0)),
            }

        return {"pending": pending, "seen": seen, "by_source": by_source}

    def clear(self) -> None:
        """
        Clear all frontier data (pending, seen, stats).

        WARNING: Use only for testing or maintenance.
        """
        self.redis.delete(self.pending_key, self.seen_key)

        # Delete all stats keys
        for key in self.redis.scan_iter(match=f"{self.stats_prefix}:*"):
            self.redis.delete(key)
