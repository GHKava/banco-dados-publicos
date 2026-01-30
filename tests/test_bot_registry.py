"""
Tests for source registry bot validators.

Note: Full SQLAlchemy ORM tests deferred due to Python 3.14 compatibility issue.
These tests validate the policy enforcement logic.
"""

from src.bots.validators import ALLOWLIST, get_source_policy_level, validate_source_policy


def test_validate_source_policy_pass_dict():
    """Test policy validation for compliant source (dict)."""
    source_dict = {
        "source_id": "SRC-001",
        "metadata": {
            "license": "CC-BY",
            "robots_respected": True,
        },
    }

    is_compliant, msg = validate_source_policy(source_dict)
    assert is_compliant is True


def test_validate_source_policy_not_in_allowlist():
    """Test policy validation rejects non-allowlisted source."""
    source_dict = {
        "source_id": "UNKNOWN",
        "metadata": {
            "license": "MIT",
            "robots_respected": True,
        },
    }

    is_compliant, msg = validate_source_policy(source_dict)
    assert is_compliant is False
    assert "not in allowlist" in msg


def test_validate_source_policy_missing_license():
    """Test policy validation rejects source without license."""
    source_dict = {
        "source_id": "SRC-001",
        "metadata": {
            "robots_respected": True,
            # Missing license!
        },
    }

    is_compliant, msg = validate_source_policy(source_dict)
    assert is_compliant is False
    assert "license" in msg.lower()


def test_validate_source_policy_robots_not_respected():
    """Test policy validation rejects source that doesn't respect robots."""
    source_dict = {
        "source_id": "SRC-001",
        "metadata": {
            "license": "CC-BY",
            "robots_respected": False,  # Does NOT respect robots!
        },
    }

    is_compliant, msg = validate_source_policy(source_dict)
    assert is_compliant is False
    assert "robots" in msg.lower()


def test_get_source_policy_level():
    """Test policy level determination."""
    metadata = {"policy_level": "FETCH_PUBLIC"}
    level = get_source_policy_level(metadata)
    assert level == "FETCH_PUBLIC"


def test_get_source_policy_level_default():
    """Test default policy level (fail-closed)."""
    metadata = {}  # No policy_level specified
    level = get_source_policy_level(metadata)
    assert level == "METADATA_ONLY"  # Fail-closed default


def test_get_source_policy_level_invalid():
    """Test invalid policy level defaults to METADATA_ONLY."""
    metadata = {"policy_level": "INVALID_LEVEL"}
    level = get_source_policy_level(metadata)
    assert level == "METADATA_ONLY"


def test_allowlist_completeness():
    """Test that all 5 sources are in allowlist."""
    expected = {"SRC-001", "SRC-002", "SRC-003", "SRC-004", "SRC-005"}
    assert ALLOWLIST == expected


def test_validate_all_allowed_sources():
    """Test that all allowlisted sources pass (with license+robots)."""
    for source_id in ALLOWLIST:
        source_dict = {
            "source_id": source_id,
            "metadata": {
                "license": "CC-BY",
                "robots_respected": True,
            },
        }

        is_compliant, msg = validate_source_policy(source_dict)
        assert is_compliant is True, f"{source_id} should be compliant"
