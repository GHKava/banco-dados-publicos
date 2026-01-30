"""
Policy validators for source registry (no SQLAlchemy imports).
"""

import logging
from typing import Any, Dict, Tuple

logger = logging.getLogger(__name__)

# Allowlist from sources.yaml
ALLOWLIST = {"SRC-001", "SRC-002", "SRC-003", "SRC-004", "SRC-005"}

# Policy defaults (fail-closed)
POLICY_DEFAULTS = {
    "policy_level": "METADATA_ONLY",  # Most restrictive
    "robots_respected": True,
    "rate_limit_requests_per_hour": 100,
}


def validate_source_policy(source: Any) -> Tuple[bool, str]:
    """
    Validate source compliance with policy.

    Fail-closed: Only explicitly allowed sources grant access.

    Args:
        source: Source dict with source_id and metadata, or Source object

    Returns:
        (is_compliant, message)
    """
    # Extract source_id and metadata (works with dict or object)
    if isinstance(source, dict):
        source_id = source.get("source_id", "unknown")
        metadata = source.get("metadata", {})
    else:
        source_id = getattr(source, "source_id", "unknown")
        metadata = getattr(source, "metadata_", {}) or {}

    # Rule 1: Check allowlist (fail-closed)
    if source_id not in ALLOWLIST:
        msg = f"Source {source_id} not in allowlist. Allowed: {ALLOWLIST}"
        logger.warning(msg)
        return False, msg

    # Rule 2: Check license
    license_metadata = metadata.get("license")
    if not license_metadata:
        msg = f"Source {source_id} missing license metadata"
        logger.warning(msg)
        return False, msg

    # Rule 3: Check robots respect
    respect_robots = metadata.get("robots_respected", POLICY_DEFAULTS["robots_respected"])
    if not respect_robots:
        msg = f"Source {source_id} does not respect robots.txt"
        logger.warning(msg)
        return False, msg

    # All checks passed
    logger.info(f"Source {source_id} passed policy validation")
    return True, "Policy compliant"


def get_source_policy_level(source_metadata: Dict) -> str:
    """
    Determine policy access level for source.

    Levels:
    - DENY: Blocked entirely (failed policy)
    - METADATA_ONLY: Only metadata allowed (default)
    - FETCH_PUBLIC: Can fetch public content
    - FULL_ACCESS: Full unrestricted access (rare)
    """
    policy = source_metadata.get("policy_level", POLICY_DEFAULTS["policy_level"])

    # Validate against known levels
    valid_levels = {"DENY", "METADATA_ONLY", "FETCH_PUBLIC", "FULL_ACCESS"}
    if policy not in valid_levels:
        logger.warning(f"Unknown policy level: {policy}, defaulting to METADATA_ONLY")
        return "METADATA_ONLY"

    return str(policy)
