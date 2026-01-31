"""
Tests for RobotsChecker.
"""

from src.bots.robots_checker import RobotsChecker


def test_robots_checker_allows_url(monkeypatch):
    checker = RobotsChecker(user_agent="TestBot/1.0")

    def fake_fetch(_url: str):
        return 200, "User-agent: *\nDisallow:\n"

    monkeypatch.setattr(checker, "_fetch_robots_txt", fake_fetch)
    result = checker.check_url("https://example.com/public")

    assert result.status == "allowed"
    assert result.allowed is True
    assert result.reason == "ok"


def test_robots_checker_blocks_disallowed_path(monkeypatch):
    checker = RobotsChecker(user_agent="TestBot/1.0")

    def fake_fetch(_url: str):
        return 200, "User-agent: *\nDisallow: /private\n"

    monkeypatch.setattr(checker, "_fetch_robots_txt", fake_fetch)
    result = checker.check_url("https://example.com/private/data")

    assert result.status == "disallowed"
    assert result.allowed is False


def test_robots_checker_handles_html_response(monkeypatch):
    checker = RobotsChecker(user_agent="TestBot/1.0")

    def fake_fetch(_url: str):
        return 200, "<!DOCTYPE html><html><body>Portal</body></html>"

    monkeypatch.setattr(checker, "_fetch_robots_txt", fake_fetch)
    result = checker.check_url("https://example.com/public")

    assert result.status == "unknown"
    assert result.allowed is None
    assert result.reason == "robots_invalid_html"


def test_robots_checker_handles_non_200(monkeypatch):
    checker = RobotsChecker(user_agent="TestBot/1.0")

    def fake_fetch(_url: str):
        return 503, ""

    monkeypatch.setattr(checker, "_fetch_robots_txt", fake_fetch)
    result = checker.check_url("https://example.com/public")

    assert result.status == "unknown"
    assert result.allowed is None
    assert result.reason == "http_status_503"


def test_robots_checker_handles_fetch_exception(monkeypatch):
    checker = RobotsChecker(user_agent="TestBot/1.0")

    def fake_fetch(_url: str):
        raise RuntimeError("timeout")

    monkeypatch.setattr(checker, "_fetch_robots_txt", fake_fetch)
    result = checker.check_url("https://example.com/public")

    assert result.status == "unknown"
    assert result.allowed is None
    assert result.reason.startswith("fetch_failed:")
