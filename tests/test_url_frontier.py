"""
Tests for URL Frontier.
"""

from unittest.mock import MagicMock

from src.bots.url_frontier import URLFrontier


class TestURLFrontier:
    """Tests for URLFrontier class"""

    def test_add_url_new(self):
        """Test adding new URL"""
        mock_redis = MagicMock()
        mock_redis.sismember.return_value = False

        frontier = URLFrontier(mock_redis)
        result = frontier.add_url("https://example.com/page", "SRC-001", priority=80)

        assert result is True
        mock_redis.sadd.assert_called_once()
        mock_redis.zadd.assert_called_once()

    def test_add_url_duplicate(self):
        """Test adding duplicate URL (dedup)"""
        mock_redis = MagicMock()
        mock_redis.sismember.return_value = True  # Already seen

        frontier = URLFrontier(mock_redis)
        result = frontier.add_url("https://example.com/page", "SRC-001")

        assert result is False
        mock_redis.sadd.assert_not_called()
        mock_redis.zadd.assert_not_called()

    def test_canonicalize_url(self):
        """Test URL canonicalization"""
        mock_redis = MagicMock()
        frontier = URLFrontier(mock_redis)

        # Test lowercase
        assert frontier._canonicalize_url("HTTP://EXAMPLE.COM/Page") == "http://example.com/Page"

        # Test default port removal
        assert (
            frontier._canonicalize_url("https://example.com:443/page") == "https://example.com/page"
        )

    def test_get_next_url(self):
        """Test popping next URL from queue"""
        mock_redis = MagicMock()
        mock_redis.zpopmax.return_value = [(b"SRC-001|https://example.com/page", 50100.0)]

        frontier = URLFrontier(mock_redis)
        url_obj = frontier.get_next_url()

        assert url_obj is not None
        assert url_obj.url == "https://example.com/page"
        assert url_obj.source_id == "SRC-001"
        assert url_obj.priority == 50

    def test_get_next_url_empty(self):
        """Test popping from empty queue"""
        mock_redis = MagicMock()
        mock_redis.zpopmax.return_value = []

        frontier = URLFrontier(mock_redis)
        url_obj = frontier.get_next_url()

        assert url_obj is None

    def test_get_queue_size(self):
        """Test getting queue size"""
        mock_redis = MagicMock()
        mock_redis.zcard.return_value = 42

        frontier = URLFrontier(mock_redis)
        size = frontier.get_queue_size()

        assert size == 42

    def test_get_seen_count(self):
        """Test getting seen count"""
        mock_redis = MagicMock()
        mock_redis.scard.return_value = 123

        frontier = URLFrontier(mock_redis)
        count = frontier.get_seen_count()

        assert count == 123

    def test_get_stats(self):
        """Test getting frontier statistics"""
        mock_redis = MagicMock()
        mock_redis.zcard.return_value = 10
        mock_redis.scard.return_value = 50
        mock_redis.scan_iter.return_value = [b"frontier:stats:SRC-001"]
        mock_redis.hgetall.return_value = {b"added": b"30", b"crawled": b"20"}

        frontier = URLFrontier(mock_redis)
        stats = frontier.get_stats()

        assert stats["pending"] == 10
        assert stats["seen"] == 50
        assert "SRC-001" in stats["by_source"]
        assert stats["by_source"]["SRC-001"]["added"] == 30
        assert stats["by_source"]["SRC-001"]["crawled"] == 20

    def test_clear(self):
        """Test clearing frontier"""
        mock_redis = MagicMock()
        mock_redis.scan_iter.return_value = [b"frontier:stats:SRC-001"]

        frontier = URLFrontier(mock_redis)
        frontier.clear()

        assert mock_redis.delete.call_count >= 2  # pending + seen + stats

    def test_compute_score(self):
        """Test score computation"""
        mock_redis = MagicMock()
        frontier = URLFrontier(mock_redis)

        # Priority 80, added 100 seconds ago
        import time

        timestamp = time.time() - 100
        score = frontier._compute_score(80, timestamp)

        # Score should be ~80000 + 100
        assert 80000 <= score <= 80200
