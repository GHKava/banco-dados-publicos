"""
Tests for Sitemap Discovery Bot.
"""

from unittest.mock import MagicMock, patch

from src.bots.discovery_sitemap import (
    SitemapURL,
    discover_from_sitemap,
    discover_from_source,
    fetch_sitemap,
    parse_sitemap,
)


class TestFetchSitemap:
    """Tests for fetch_sitemap function"""

    @patch("src.bots.discovery_sitemap.requests.get")
    def test_fetch_sitemap_success(self, mock_get):
        """Test successful sitemap fetch"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/xml"}
        mock_response.text = "<urlset></urlset>"
        mock_get.return_value = mock_response

        result = fetch_sitemap("https://example.com/sitemap.xml")

        assert result == "<urlset></urlset>"

    @patch("src.bots.discovery_sitemap.requests.get")
    def test_fetch_sitemap_404(self, mock_get):
        """Test sitemap not found (404)"""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = fetch_sitemap("https://example.com/sitemap.xml")

        assert result is None

    @patch("src.bots.discovery_sitemap.requests.get")
    def test_fetch_sitemap_not_xml(self, mock_get):
        """Test non-XML response"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.text = "<html></html>"
        mock_get.return_value = mock_response

        result = fetch_sitemap("https://example.com/sitemap.xml")

        assert result is None

    @patch("src.bots.discovery_sitemap.requests.get")
    def test_fetch_sitemap_timeout(self, mock_get):
        """Test fetch timeout"""
        import requests

        mock_get.side_effect = requests.RequestException("Timeout")

        result = fetch_sitemap("https://example.com/sitemap.xml")

        assert result is None


class TestParseSitemap:
    """Tests for parse_sitemap function"""

    def test_parse_sitemap_urlset(self):
        """Test parsing standard sitemap (urlset)"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/page1</loc>
    <lastmod>2024-01-01</lastmod>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://example.com/page2</loc>
  </url>
</urlset>"""

        urls = parse_sitemap(xml_content)

        assert len(urls) == 2
        assert urls[0].loc == "https://example.com/page1"
        assert urls[0].lastmod == "2024-01-01"
        assert urls[0].priority == 0.8
        assert urls[1].loc == "https://example.com/page2"

    def test_parse_sitemap_index(self):
        """Test parsing sitemap index"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemap1.xml</loc>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemap2.xml</loc>
  </sitemap>
</sitemapindex>"""

        urls = parse_sitemap(xml_content)

        assert len(urls) == 2
        assert urls[0].loc == "https://example.com/sitemap1.xml"
        assert urls[1].loc == "https://example.com/sitemap2.xml"

    def test_parse_sitemap_malformed(self):
        """Test parsing malformed XML"""
        xml_content = "<urlset><url><loc>broken</url></urlset>"

        urls = parse_sitemap(xml_content)

        assert urls == []

    def test_parse_sitemap_empty(self):
        """Test parsing empty sitemap"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
</urlset>"""

        urls = parse_sitemap(xml_content)

        assert urls == []


class TestDiscoverFromSitemap:
    """Tests for discover_from_sitemap function"""

    @patch("src.bots.discovery_sitemap.fetch_sitemap")
    def test_discover_from_sitemap_simple(self, mock_fetch):
        """Test discovering from simple sitemap"""
        mock_fetch.return_value = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/page1</loc></url>
  <url><loc>https://example.com/page2</loc></url>
</urlset>"""

        urls = discover_from_sitemap("https://example.com/sitemap.xml")

        assert len(urls) == 2
        assert urls[0].loc == "https://example.com/page1"

    @patch("src.bots.discovery_sitemap.fetch_sitemap")
    def test_discover_from_sitemap_index(self, mock_fetch):
        """Test discovering from sitemap index (recursive)"""

        def mock_fetch_side_effect(url):
            if url == "https://example.com/sitemap.xml":
                return """<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://example.com/sitemap1.xml</loc></sitemap>
</sitemapindex>"""
            elif url == "https://example.com/sitemap1.xml":
                return """<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://example.com/page1</loc></url>
</urlset>"""
            return None

        mock_fetch.side_effect = mock_fetch_side_effect

        urls = discover_from_sitemap("https://example.com/sitemap.xml")

        assert len(urls) == 1
        assert urls[0].loc == "https://example.com/page1"

    @patch("src.bots.discovery_sitemap.fetch_sitemap")
    def test_discover_from_sitemap_max_depth(self, mock_fetch):
        """Test max depth limit for sitemap index"""
        mock_fetch.return_value = """<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://example.com/sitemap1.xml</loc></sitemap>
</sitemapindex>"""

        urls = discover_from_sitemap("https://example.com/sitemap.xml", max_depth=0)

        assert urls == []  # Max depth reached immediately


class TestDiscoverFromSource:
    """Tests for discover_from_source function"""

    @patch("src.bots.discovery_sitemap.discover_from_sitemap")
    def test_discover_from_source(self, mock_discover):
        """Test discovering from source with explicit sitemap_urls"""
        mock_discover.return_value = [SitemapURL(loc="https://example.com/page1")]

        sources_config = {
            "sources": [
                {
                    "source_id": "SRC-TEST",
                    "base_domains": ["example.com"],
                    "sitemap_urls": ["https://example.com/sitemap.xml"],
                }
            ]
        }

        urls = discover_from_source("SRC-TEST", sources_config)

        assert len(urls) == 1
        assert urls[0].loc == "https://example.com/page1"

    @patch("src.bots.discovery_sitemap.discover_from_sitemap")
    def test_discover_from_source_infer_sitemap(self, mock_discover):
        """Test discovering from source with inferred sitemap.xml"""
        mock_discover.return_value = [SitemapURL(loc="https://example.com/page1")]

        sources_config = {
            "sources": [
                {
                    "source_id": "SRC-TEST",
                    "base_domains": ["example.com"],
                    # No sitemap_urls specified
                }
            ]
        }

        urls = discover_from_source("SRC-TEST", sources_config)

        assert len(urls) == 1
        mock_discover.assert_called_once_with("https://example.com/sitemap.xml")

    def test_discover_from_source_not_found(self):
        """Test discovering from non-existent source"""
        sources_config = {"sources": []}

        urls = discover_from_source("SRC-INVALID", sources_config)

        assert urls == []
