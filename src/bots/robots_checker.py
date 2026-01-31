"""
Robots.txt checker for source compliance.

Provides a small utility to fetch robots.txt and evaluate URL access
for a given user agent. Designed to be conservative and report
"unknown" when robots.txt is missing or invalid.
"""

from __future__ import annotations

import logging
import urllib.robotparser
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)


@dataclass
class RobotsCheckResult:
    """Result of robots.txt evaluation for a URL."""

    url: str
    robots_url: str
    status: str  # allowed | disallowed | unknown
    allowed: Optional[bool]
    http_status: Optional[int]
    reason: str
    crawl_delay_s: Optional[float]
    sitemaps: list[str]


class RobotsChecker:
    """Fetch and evaluate robots.txt for a target URL."""

    def __init__(self, user_agent: str = "PublicDataPipelineBot/1.0", timeout_s: int = 20):
        self.user_agent = user_agent
        self.timeout_s = timeout_s

    def check_url(self, url: str) -> RobotsCheckResult:
        """Check whether the given URL is allowed by robots.txt."""
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        try:
            http_status, content = self._fetch_robots_txt(robots_url)
        except Exception as exc:  # pragma: no cover - network failure path
            logger.warning("robots.txt fetch failed: %s", exc)
            return RobotsCheckResult(
                url=url,
                robots_url=robots_url,
                status="unknown",
                allowed=None,
                http_status=None,
                reason=f"fetch_failed: {exc}",
                crawl_delay_s=None,
                sitemaps=[],
            )

        if http_status != 200:
            return RobotsCheckResult(
                url=url,
                robots_url=robots_url,
                status="unknown",
                allowed=None,
                http_status=http_status,
                reason=f"http_status_{http_status}",
                crawl_delay_s=None,
                sitemaps=[],
            )

        if self._looks_like_html(content):
            return RobotsCheckResult(
                url=url,
                robots_url=robots_url,
                status="unknown",
                allowed=None,
                http_status=http_status,
                reason="robots_invalid_html",
                crawl_delay_s=None,
                sitemaps=[],
            )

        rp = self._parse_robots_txt(content)
        allowed = rp.can_fetch(self.user_agent, url)
        raw_crawl_delay = rp.crawl_delay(self.user_agent)
        crawl_delay: Optional[float] = None
        if raw_crawl_delay is not None:
            try:
                crawl_delay = float(raw_crawl_delay)
            except (TypeError, ValueError):
                crawl_delay = None
        sitemaps = rp.site_maps() or []

        return RobotsCheckResult(
            url=url,
            robots_url=robots_url,
            status="allowed" if allowed else "disallowed",
            allowed=allowed,
            http_status=http_status,
            reason="ok",
            crawl_delay_s=crawl_delay,
            sitemaps=sitemaps,
        )

    def _fetch_robots_txt(self, robots_url: str) -> tuple[int, str]:
        """Fetch robots.txt content from URL."""
        req = Request(robots_url, headers={"User-Agent": self.user_agent})
        with urlopen(req, timeout=self.timeout_s) as response:
            status = response.getcode() or 0
            content = response.read().decode("utf-8", errors="replace")
        return status, content

    @staticmethod
    def _parse_robots_txt(content: str) -> urllib.robotparser.RobotFileParser:
        """Parse robots.txt content into RobotFileParser."""
        rp = urllib.robotparser.RobotFileParser()
        rp.parse(content.splitlines())
        return rp

    @staticmethod
    def _looks_like_html(content: str) -> bool:
        """Detect HTML responses served in place of robots.txt."""
        snippet = content.lstrip().lower()
        return snippet.startswith("<!doctype html") or snippet.startswith("<html")
