"""
RSS Discovery Bot

Fetches and parses RSS/Atom feeds to discover URLs for crawling.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional

import feedparser
import requests

logger = logging.getLogger(__name__)


@dataclass
class FeedEntry:
    """Entry discovered from RSS/Atom feed."""

    link: str
    title: Optional[str] = None
    published: Optional[str] = None
    summary: Optional[str] = None


def fetch_feed(url: str, timeout: int = 30) -> Optional[str]:
    """
    Fetch feed content.

    Args:
        url: Feed URL (e.g., https://example.com/feed)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        Feed content as string, or None if fetch failed
    """
    try:
        response = requests.get(
            url, timeout=timeout, headers={"User-Agent": "PublicDataPipelineBot/1.0"}
        )

        if response.status_code != 200:
            logger.warning(f"Feed fetch failed: {url} (status {response.status_code})")
            return None

        return response.text

    except requests.RequestException as e:
        logger.error(f"Failed to fetch feed {url}: {e}")
        return None


def parse_feed(content: str) -> List[FeedEntry]:
    """
    Parse feed content (RSS or Atom).

    Args:
        content: Feed content as string

    Returns:
        List of FeedEntry objects
    """
    try:
        feed = feedparser.parse(content)
    except Exception as e:
        logger.error(f"Failed to parse feed: {e}")
        return []

    if feed.bozo:  # feedparser detected malformed feed
        logger.warning(f"Feed malformed (bozo=True): {feed.bozo_exception}")

    entries = []

    for entry in feed.entries:
        # Extract link (required)
        link = entry.get("link")
        if not link:
            continue

        # Extract metadata (optional)
        title = entry.get("title")
        published = entry.get("published", entry.get("updated"))
        summary = entry.get("summary", entry.get("description"))

        entries.append(FeedEntry(link=link, title=title, published=published, summary=summary))

    return entries


def discover_from_feed(feed_url: str) -> List[FeedEntry]:
    """
    Discover URLs from feed.

    Args:
        feed_url: Feed URL

    Returns:
        List of FeedEntry objects
    """
    # Fetch feed
    content = fetch_feed(feed_url)
    if not content:
        return []

    # Parse feed
    entries = parse_feed(content)

    logger.info(f"Discovered {len(entries)} entries from feed: {feed_url}")
    return entries


def discover_from_source(source_id: str, sources_config: dict) -> List[FeedEntry]:
    """
    Discover URLs from source's feeds (uses sources.yaml).

    Args:
        source_id: Source ID (e.g., 'SRC-001')
        sources_config: Loaded sources.yaml dict

    Returns:
        List of FeedEntry objects

    Example:
        >>> config = yaml.safe_load(open('configs/sources.yaml'))
        >>> entries = discover_from_source('SRC-002', config)
        >>> len(entries)
        50
    """
    # Find source in config
    source = next(
        (s for s in sources_config.get("sources", []) if s["source_id"] == source_id), None
    )
    if not source:
        logger.error(f"Source {source_id} not found in sources.yaml")
        return []

    # Get feed URLs (explicit or infer)
    feed_urls = source.get("feed_urls", [])

    if not feed_urls:
        # Infer default feed URLs
        base_domain = source["base_domains"][0]
        feed_urls = [f"https://{base_domain}/feed", f"https://{base_domain}/rss"]

    # Discover from all feeds
    all_entries = []
    for feed_url in feed_urls:
        entries = discover_from_feed(feed_url)
        all_entries.extend(entries)

    logger.info(f"Discovered {len(all_entries)} entries from {source_id} feeds")
    return all_entries
