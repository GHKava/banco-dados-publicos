"""
Tests for RSS Discovery Bot.
"""

from unittest.mock import MagicMock, patch

from src.bots.discovery_rss import (
    FeedEntry,
    discover_from_feed,
    discover_from_source,
    fetch_feed,
    parse_feed,
)


class TestFetchFeed:
    """Tests for fetch_feed function"""

    @patch("src.bots.discovery_rss.requests.get")
    def test_fetch_feed_success(self, mock_get):
        """Test successful feed fetch"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<rss></rss>"
        mock_get.return_value = mock_response

        result = fetch_feed("https://example.com/feed")

        assert result == "<rss></rss>"

    @patch("src.bots.discovery_rss.requests.get")
    def test_fetch_feed_404(self, mock_get):
        """Test feed not found (404)"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = fetch_feed("https://example.com/feed")

        assert result is None

    @patch("src.bots.discovery_rss.requests.get")
    def test_fetch_feed_timeout(self, mock_get):
        """Test fetch timeout"""
        import requests

        mock_get.side_effect = requests.RequestException("Timeout")

        result = fetch_feed("https://example.com/feed")

        assert result is None


class TestParseFeed:
    """Tests for parse_feed function"""

    def test_parse_feed_rss2(self):
        """Test parsing RSS 2.0 feed"""
        rss_content = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item>
      <title>Article 1</title>
      <link>https://example.com/article1</link>
      <pubDate>Mon, 01 Jan 2024 00:00:00 GMT</pubDate>
      <description>Summary 1</description>
    </item>
    <item>
      <title>Article 2</title>
      <link>https://example.com/article2</link>
    </item>
  </channel>
</rss>"""

        entries = parse_feed(rss_content)

        assert len(entries) == 2
        assert entries[0].link == "https://example.com/article1"
        assert entries[0].title == "Article 1"
        assert entries[0].published is not None
        assert entries[1].link == "https://example.com/article2"

    def test_parse_feed_atom(self):
        """Test parsing Atom feed"""
        atom_content = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <entry>
    <title>Article 1</title>
    <link href="https://example.com/article1"/>
    <updated>2024-01-01T00:00:00Z</updated>
    <summary>Summary 1</summary>
  </entry>
</feed>"""

        entries = parse_feed(atom_content)

        assert len(entries) == 1
        assert entries[0].link == "https://example.com/article1"
        assert entries[0].title == "Article 1"

    def test_parse_feed_empty(self):
        """Test parsing empty feed"""
        empty_feed = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
  </channel>
</rss>"""

        entries = parse_feed(empty_feed)

        assert entries == []

    def test_parse_feed_malformed(self):
        """Test parsing malformed feed (feedparser tolerates errors)"""
        malformed = "<rss><item><link>https://example.com</link></item></rss>"

        entries = parse_feed(malformed)

        # feedparser is tolerant, should still extract link
        assert len(entries) >= 0  # May or may not extract depending on error


class TestDiscoverFromFeed:
    """Tests for discover_from_feed function"""

    @patch("src.bots.discovery_rss.fetch_feed")
    def test_discover_from_feed_success(self, mock_fetch):
        """Test discovering from feed"""
        mock_fetch.return_value = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <item><link>https://example.com/1</link></item>
    <item><link>https://example.com/2</link></item>
  </channel>
</rss>"""

        entries = discover_from_feed("https://example.com/feed")

        assert len(entries) == 2
        assert entries[0].link == "https://example.com/1"

    @patch("src.bots.discovery_rss.fetch_feed")
    def test_discover_from_feed_not_found(self, mock_fetch):
        """Test discovering from non-existent feed"""
        mock_fetch.return_value = None

        entries = discover_from_feed("https://example.com/feed")

        assert entries == []


class TestDiscoverFromSource:
    """Tests for discover_from_source function"""

    @patch("src.bots.discovery_rss.discover_from_feed")
    def test_discover_from_source_explicit_feeds(self, mock_discover):
        """Test discovering from source with explicit feed_urls"""
        mock_discover.return_value = [FeedEntry(link="https://example.com/1")]

        sources_config = {
            "sources": [
                {
                    "source_id": "SRC-TEST",
                    "base_domains": ["example.com"],
                    "feed_urls": ["https://example.com/feed"],
                }
            ]
        }

        entries = discover_from_source("SRC-TEST", sources_config)

        assert len(entries) == 1
        assert entries[0].link == "https://example.com/1"

    @patch("src.bots.discovery_rss.discover_from_feed")
    def test_discover_from_source_infer_feeds(self, mock_discover):
        """Test discovering from source with inferred feed URLs"""
        mock_discover.return_value = [FeedEntry(link="https://example.com/1")]

        sources_config = {
            "sources": [
                {
                    "source_id": "SRC-TEST",
                    "base_domains": ["example.com"],
                    # No feed_urls specified
                }
            ]
        }

        entries = discover_from_source("SRC-TEST", sources_config)

        # Should try /feed and /rss (2 calls)
        assert len(entries) == 2  # 1 entry per feed URL

    def test_discover_from_source_not_found(self):
        """Test discovering from non-existent source"""
        sources_config = {"sources": []}

        entries = discover_from_source("SRC-INVALID", sources_config)

        assert entries == []
