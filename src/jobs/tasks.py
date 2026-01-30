"""
Example job for RQ.

Demonstrates simple job processing.
"""

import logging
from datetime import datetime

logger = logging.getLogger(__name__)


def example_job(x: int, y: int) -> int:
    """Simple example job: add two numbers."""
    result = x + y
    logger.info(f"Example job: {x} + {y} = {result}")
    return result


def fetch_source_task(source_id: str) -> dict:
    """Example: fetch data from a source."""
    logger.info(f"Fetching from source: {source_id}")

    # Simulated work
    result = {
        "source_id": source_id,
        "fetched_at": datetime.utcnow().isoformat(),
        "status": "success",
        "count": 0,
    }

    logger.info(f"Fetch complete: {result}")
    return result


def process_document_task(doc_id: str) -> dict:
    """Example: process a document."""
    logger.info(f"Processing document: {doc_id}")

    result = {
        "doc_id": doc_id,
        "status": "cleaned",
        "chunks": 0,
    }

    logger.info(f"Processing complete: {result}")
    return result
