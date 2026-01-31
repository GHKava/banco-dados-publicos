"""
Generic scraper for public data sources defined in `configs/sources.yaml`.

This script reads the YAML configuration file produced earlier and attempts to
download the primary entrypoint for each data source. The goal is to
provide a starting point for further development; given the diversity of
sources (APIs, HTML pages, PDF journals, dumps), it is not feasible to
completely automate extraction of all information with one generic
script. Instead, the script performs the following:

1. Loads the list of sources from `configs/sources.yaml` using PyYAML.
2. For each source, iterates through the list of entrypoints.
3. Uses Python's `urllib.robotparser` to parse the site's `robots.txt` (if
   available) and checks whether the entrypoint URL is allowed for a
   generic user agent (configured below). If the path is disallowed, the
   script skips the request and logs a warning.
4. Issues an HTTP GET request using the `requests` library (if
   installed) or `urllib.request` as a fallback. The request includes a
   custom `User-Agent` header. The script waits an appropriate amount of
   time between requests based on the `rate_limit_rps` defined in the
   YAML configuration (defaulting to 1 request per second when
   unspecified).
5. Saves the response content to a file inside an `output` directory,
   organized by `source_id`. The filename is derived from the URL path
   (e.g., `index.html`, `data.json`). If the response has a JSON content
   type, the script attempts to pretty-print and save it as JSON.

Limitations:
• This script does not attempt to parse or process the downloaded data.
• It does not handle APIs requiring authentication, pagination or
  complex query parameters; only the base entrypoint is fetched.
• For HTML pages or dumps that link to multiple files, the script
  downloads only the initial page. Extending the logic for full-site
  scraping will require per‑source customization.
• The script respects the `robots.txt` file but does not handle
  site‑specific rate limits beyond the generic rate configured in the
  YAML.

To run:
```
python scrape_all_sources.py
```

Dependencies: Requires PyYAML and the `requests` library. If `requests` is
not installed, the script falls back to `urllib.request` but cannot
download HTTPS sites with invalid certificates.
"""

import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
import urllib.robotparser
import urllib.request

try:
    import yaml  # type: ignore
except ImportError:
    print("PyYAML is not installed. Please install it with 'pip install pyyaml'.")
    sys.exit(1)

try:
    import requests  # type: ignore
except ImportError:
    requests = None  # fallback to urllib


USER_AGENT = "PublicDataScraper/1.0 (+https://example.com)"


@dataclass
class Source:
    source_id: str
    name: str
    base_domains: list[str]
    entrypoints: list[str]
    rate_limit_rps: float


def load_sources(yaml_path: Path) -> list[Source]:
    """Load sources from YAML configuration, returning a list of Source objects."""
    with yaml_path.open('r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    sources: list[Source] = []
    for item in data:
        rate = item.get('crawl_policy', {}).get('rate_limit_rps', 1.0)
        entrypoints = item.get('entrypoints', []) or []
        # Ensure we have at least one entrypoint
        if not entrypoints:
            continue
        sources.append(
            Source(
                source_id=item['source_id'],
                name=item['name'],
                base_domains=item.get('base_domains', []),
                entrypoints=entrypoints,
                rate_limit_rps=rate if rate else 1.0,
            )
        )
    return sources


def is_url_allowed(url: str, user_agent: str) -> bool:
    """Check robots.txt for the given URL. Returns True if allowed or
    robots.txt is unreachable/unavailable."""
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
    except Exception:
        # If robots.txt cannot be read, be conservative and allow
        return True
    return rp.can_fetch(user_agent, url)


def fetch_url(url: str) -> tuple[bytes, str]:
    """Fetch content from a URL. Returns (content, content_type)."""
    headers = {"User-Agent": USER_AGENT}
    if requests:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        content_type = resp.headers.get('Content-Type', '')
        return resp.content, content_type
    else:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=30) as resp:
            content_type = resp.headers.get('Content-Type', '')
            data = resp.read()
        return data, content_type


def save_content(src: Source, url: str, content: bytes, content_type: str, out_dir: Path) -> None:
    """Save content to a file derived from the URL path inside out_dir."""
    parsed = urlparse(url)
    # Use path or default to index
    path = parsed.path.strip('/') or 'index'
    # Replace slashes with underscores
    filename = re.sub(r'[/\\]+', '_', path)
    # Append extension based on content_type
    if 'json' in content_type.lower():
        filename += '.json'
        try:
            obj = json.loads(content.decode('utf-8'))
            with (out_dir / filename).open('w', encoding='utf-8') as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)
            return
        except Exception:
            pass  # fall back to binary write
    elif 'html' in content_type.lower():
        filename += '.html'
    elif 'pdf' in content_type.lower():
        filename += '.pdf'
    # Save binary data
    with (out_dir / filename).open('wb') as f:
        f.write(content)


def scrape_sources(config_path: str = 'configs/sources.yaml', output_root: str = 'output') -> None:
    """Main entry point: load sources and fetch each entrypoint."""
    sources = load_sources(Path(config_path))
    out_base = Path(output_root)
    out_base.mkdir(parents=True, exist_ok=True)
    for src in sources:
        src_dir = out_base / src.source_id
        src_dir.mkdir(exist_ok=True)
        for url in src.entrypoints:
            print(f"[{src.source_id}] Downloading {url}...")
            if not is_url_allowed(url, USER_AGENT):
                print(f"  Skipped due to robots.txt restriction: {url}")
                continue
            try:
                content, ctype = fetch_url(url)
                save_content(src, url, content, ctype, src_dir)
                print(f"  Saved content (type: {ctype})")
            except Exception as e:
                print(f"  Error fetching {url}: {e}")
            # Respect rate limit
            delay = 1.0 / src.rate_limit_rps if src.rate_limit_rps > 0 else 1.0
            time.sleep(delay)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Scrape entrypoints from public data sources.')
    parser.add_argument('-c', '--config', default='configs/sources.yaml', help='Path to the YAML configuration file.')
    parser.add_argument('-o', '--output', default='output', help='Directory to save downloaded content.')
    args = parser.parse_args()
    scrape_sources(args.config, args.output)