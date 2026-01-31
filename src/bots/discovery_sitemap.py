"""
Sitemap Discovery Bot

Fetches and parses sitemaps XML to discover URLs for crawling.
"""

import logging
from dataclasses import dataclass
from typing import List, Optional
from xml.etree import ElementTree as ET

import requests

logger = logging.getLogger(__name__)


@dataclass
class SitemapURL:
    """URL discovered from sitemap."""

    loc: str
    lastmod: Optional[str] = None
    priority: Optional[float] = None
    changefreq: Optional[str] = None


def fetch_sitemap(url: str, timeout: int = 30) -> Optional[str]:
    """
    Fetch sitemap XML content.

    Args:
        url: Sitemap URL (e.g., https://example.com/sitemap.xml)
        timeout: Request timeout in seconds (default: 30)

    Returns:
        XML content as string, or None if fetch failed
    """
    try:
        response = requests.get(
            url, timeout=timeout, headers={"User-Agent": "PublicDataPipelineBot/1.0"}
        )

        if response.status_code != 200:
            logger.warning(f"Sitemap fetch failed: {url} (status {response.status_code})")
            return None

        # Check if response is XML
        content_type = response.headers.get("Content-Type", "")
        if "xml" not in content_type.lower():
            logger.warning(f"Sitemap not XML: {url} (content-type: {content_type})")
            return None

        return response.text

    except requests.RequestException as e:
        logger.error(f"Failed to fetch sitemap {url}: {e}")
        return None


def parse_sitemap(xml_content: str) -> List[SitemapURL]:
    """
    Parse sitemap XML and extract URLs.

    Supports:
    - Standard sitemap (urlset)
    - Sitemap index (sitemapindex)

    Args:
        xml_content: XML content as string

    Returns:
        List of SitemapURL objects
    """
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as e:
        logger.error(f"Failed to parse sitemap XML: {e}")
        return []

    # Namespace handling (sitemaps.org)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

    urls = []

    # Check if sitemap index
    if root.tag.endswith("sitemapindex"):
        # Extract sitemap URLs (recursive fetch needed)
        for sitemap_elem in root.findall("sm:sitemap", ns):
            loc_elem = sitemap_elem.find("sm:loc", ns)
            if loc_elem is not None and loc_elem.text:
                urls.append(SitemapURL(loc=loc_elem.text))

    # Standard sitemap (urlset)
    elif root.tag.endswith("urlset"):
        for url_elem in root.findall("sm:url", ns):
            loc_elem = url_elem.find("sm:loc", ns)
            if loc_elem is None or not loc_elem.text:
                continue

            lastmod_elem = url_elem.find("sm:lastmod", ns)
            priority_elem = url_elem.find("sm:priority", ns)
            changefreq_elem = url_elem.find("sm:changefreq", ns)

            url_obj = SitemapURL(
                loc=loc_elem.text,
                lastmod=lastmod_elem.text if lastmod_elem is not None else None,
                priority=(
                    float(priority_elem.text)
                    if priority_elem is not None and priority_elem.text
                    else None
                ),
                changefreq=changefreq_elem.text if changefreq_elem is not None else None,
            )
            urls.append(url_obj)

    else:
        logger.warning(f"Unknown sitemap root tag: {root.tag}")

    return urls


def discover_from_sitemap(
    sitemap_url: str, max_depth: int = 2, current_depth: int = 0
) -> List[SitemapURL]:
    """
    Discover URLs from sitemap (with recursive sitemap index support).

    Args:
        sitemap_url: URL of sitemap or sitemap index
        max_depth: Maximum recursion depth for sitemap index (default: 2)
        current_depth: Current recursion depth (internal)

    Returns:
        List of SitemapURL objects (URLs discovered)
    """
    if current_depth >= max_depth:
        logger.warning(f"Max sitemap depth reached ({max_depth}): {sitemap_url}")
        return []

    # Fetch sitemap
    xml_content = fetch_sitemap(sitemap_url)
    if not xml_content:
        return []

    # Parse sitemap
    urls = parse_sitemap(xml_content)

    # Check if sitemap index (recursive fetch)
    if urls and all(url.loc.endswith(".xml") for url in urls[:3]):  # Heuristic: all URLs are .xml
        logger.info(f"Sitemap index detected: {sitemap_url} ({len(urls)} sub-sitemaps)")

        all_urls = []
        for sub_sitemap in urls:
            sub_urls = discover_from_sitemap(sub_sitemap.loc, max_depth, current_depth + 1)
            all_urls.extend(sub_urls)

        return all_urls

    return urls


def discover_from_source(source_id: str, sources_config: dict) -> List[SitemapURL]:
    """
    Discover URLs from source's sitemap (uses sources.yaml).

    Args:
        source_id: Source ID (e.g., 'SRC-001')
        sources_config: Loaded sources.yaml dict

    Returns:
        List of SitemapURL objects

    Example:
        >>> config = yaml.safe_load(open('configs/sources.yaml'))
        >>> urls = discover_from_source('SRC-002', config)
        >>> len(urls)
        150
    """
    # Find source in config
    source = next(
        (s for s in sources_config.get("sources", []) if s["source_id"] == source_id), None
    )
    if not source:
        logger.error(f"Source {source_id} not found in sources.yaml")
        return []

    # Get sitemap URLs (explicit or infer)
    sitemap_urls = source.get("sitemap_urls", [])

    if not sitemap_urls:
        # Infer default sitemap.xml
        base_domain = source["base_domains"][0]
        sitemap_urls = [f"https://{base_domain}/sitemap.xml"]

    # Discover from all sitemaps
    all_urls = []
    for sitemap_url in sitemap_urls:
        urls = discover_from_sitemap(sitemap_url)
        all_urls.extend(urls)

    logger.info(f"Discovered {len(all_urls)} URLs from {source_id} sitemaps")
    return all_urls
