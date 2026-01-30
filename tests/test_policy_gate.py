"""
Tests for policy gate module.
"""

import pytest

from src.bots.policy_gate import ALLOWLIST, PolicyDecision, PolicyGate


@pytest.fixture
def policy_gate():
    """Create PolicyGate instance for testing."""
    return PolicyGate(fail_closed=True)


def test_policy_gate_imports():
    """Test that PolicyGate can be imported."""
    assert PolicyGate is not None
    assert PolicyDecision is not None


def test_policy_decision_enum():
    """Test PolicyDecision enum values."""
    assert PolicyDecision.ALLOW == "ALLOW"
    assert PolicyDecision.METADATA_ONLY == "METADATA_ONLY"
    assert PolicyDecision.BLOCK == "BLOCK"


def test_allowlist_populated():
    """Test that allowlist is populated with expected sources."""
    assert len(ALLOWLIST) == 5
    assert "SRC-001" in ALLOWLIST
    assert "SRC-005" in ALLOWLIST


def test_evaluate_source_not_in_allowlist(policy_gate):
    """Test that sources not in allowlist are BLOCKED."""
    source = {
        "source_id": "SRC-999",
        "url": "https://example.com",
        "metadata": {},
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.BLOCK


def test_evaluate_source_in_allowlist_no_license(policy_gate):
    """Test that source in allowlist without license → METADATA_ONLY (fail-closed)."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {},
    }
    decision = policy_gate.evaluate(source)
    # Missing license on .gov.br domain → METADATA_ONLY (benefit of doubt)
    assert decision == PolicyDecision.METADATA_ONLY


def test_evaluate_source_with_permissive_license(policy_gate):
    """Test that source with permissive license → ALLOW."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {
            "license_policy": {
                "license_type": "public_domain",
                "license_status": "verified",
            }
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.ALLOW


def test_evaluate_source_license_unknown(policy_gate):
    """Test that source with unknown license → METADATA_ONLY."""
    source = {
        "source_id": "SRC-002",
        "url": "https://planalto.gov.br",
        "metadata": {
            "license_policy": {
                "license_status": "unknown",
            }
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.METADATA_ONLY


def test_evaluate_source_robots_disallow(policy_gate):
    """Test that robots.txt Disallow → BLOCK."""
    source = {
        "source_id": "SRC-003",
        "url": "https://ibge.gov.br",
        "metadata": {
            "robots_disallow": True,
            "license_policy": {
                "license_type": "open_government_license",
                "license_status": "verified",
            },
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.BLOCK


def test_evaluate_source_high_crawl_delay(policy_gate):
    """Test that high crawl_delay → METADATA_ONLY."""
    source = {
        "source_id": "SRC-004",
        "url": "https://bcb.gov.br",
        "metadata": {
            "crawl_policy": {
                "crawl_delay_s": 10,  # >5s
            },
            "license_policy": {
                "license_type": "cc-by",
                "license_status": "verified",
            },
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.METADATA_ONLY


def test_evaluate_source_tos_prohibited(policy_gate):
    """Test that ToS prohibits scraping → BLOCK."""
    source = {
        "source_id": "SRC-005",
        "url": "https://dados.gov.br",
        "metadata": {
            "tos": {
                "scraping_allowed": "prohibited",
            },
            "license_policy": {
                "license_type": "open_government_license",
                "license_status": "verified",
            },
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.BLOCK


def test_evaluate_source_high_pii_with_redaction(policy_gate):
    """Test that high PII with redaction → METADATA_ONLY (conservative)."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {
            "data_handling": {
                "pii_expected": "high",
                "pii_actions": ["detect", "redact"],
            },
            "license_policy": {
                "license_type": "public_domain",
                "license_status": "verified",
            },
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.METADATA_ONLY


def test_evaluate_source_high_pii_no_redaction(policy_gate):
    """Test that high PII without redaction → BLOCK."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {
            "data_handling": {
                "pii_expected": "high",
                "pii_actions": [],  # No mitigation
            },
            "license_policy": {
                "license_type": "public_domain",
                "license_status": "verified",
            },
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.BLOCK


def test_evaluate_source_medium_pii(policy_gate):
    """Test that medium PII → METADATA_ONLY."""
    source = {
        "source_id": "SRC-002",
        "url": "https://planalto.gov.br",
        "metadata": {
            "data_handling": {
                "pii_expected": "medium",
            },
            "license_policy": {
                "license_type": "government_open_data",
                "license_status": "verified",
            },
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.METADATA_ONLY


def test_evaluate_source_low_pii_permissive_license(policy_gate):
    """Test that low PII + permissive license → ALLOW."""
    source = {
        "source_id": "SRC-003",
        "url": "https://ibge.gov.br",
        "metadata": {
            "data_handling": {
                "pii_expected": "low",
            },
            "license_policy": {
                "license_type": "cc0",
                "license_status": "verified",
            },
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.ALLOW


def test_evaluate_source_explicit_storage_mode_block(policy_gate):
    """Test explicit storage mode BLOCK in license_policy."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {
            "license_policy": {
                "default_storage_mode": "BLOCK",
            }
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.BLOCK


def test_evaluate_source_explicit_storage_mode_metadata_only(policy_gate):
    """Test explicit storage mode METADATA_ONLY in license_policy."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {
            "license_policy": {
                "default_storage_mode": "METADATA_ONLY",
            }
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.METADATA_ONLY


def test_evaluate_source_explicit_storage_mode_allow(policy_gate):
    """Test explicit storage mode ALLOW in license_policy."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {
            "license_policy": {
                "default_storage_mode": "ALLOW",
            }
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.ALLOW


def test_evaluate_source_missing_robots_gov_domain(policy_gate):
    """Test missing robots.txt on .gov domain → ALLOW (typical gov behavior)."""
    source = {
        "source_id": "SRC-004",
        "url": "https://bcb.gov.br",
        "metadata": {
            "license_policy": {
                "license_type": "open_government_license",
                "license_status": "verified",
            },
            # No robots info → default to ALLOW for gov
        },
    }
    decision = policy_gate.evaluate(source)
    assert decision == PolicyDecision.ALLOW


def test_check_allowlist_method(policy_gate):
    """Test _check_allowlist method directly."""
    assert policy_gate._check_allowlist("SRC-001") is True
    assert policy_gate._check_allowlist("SRC-999") is False


def test_extract_source_fields_dict(policy_gate):
    """Test _extract_source_fields with dict input."""
    source = {
        "source_id": "SRC-001",
        "url": "https://in.gov.br",
        "metadata": {"key": "value"},
    }
    source_id, metadata, base_url = policy_gate._extract_source_fields(source)
    assert source_id == "SRC-001"
    assert metadata == {"key": "value"}
    assert base_url == "https://in.gov.br"


def test_extract_source_fields_object(policy_gate):
    """Test _extract_source_fields with object input."""

    class MockSource:
        source_id = "SRC-002"
        url = "https://planalto.gov.br"
        metadata_ = {"license": "cc0"}

    source = MockSource()
    source_id, metadata, base_url = policy_gate._extract_source_fields(source)
    assert source_id == "SRC-002"
    assert metadata == {"license": "cc0"}
    assert base_url == "https://planalto.gov.br"
