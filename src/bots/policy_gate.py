"""
Policy gate module for automated compliance decisions.

This module implements the PolicyGate class which evaluates sources
and determines access level: ALLOW, METADATA_ONLY, or BLOCK.

Fail-closed by default: unclear compliance → METADATA_ONLY
"""

import logging
from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple
from uuid import UUID

logger = logging.getLogger(__name__)


class PolicyDecision(str, Enum):
    """Policy gate decision outcomes."""

    ALLOW = "ALLOW"  # Full text storage permitted
    METADATA_ONLY = "METADATA_ONLY"  # Only metadata/links (default)
    BLOCK = "BLOCK"  # No ingestion permitted


# Allowlist from sources.yaml (SRC-001 to SRC-005)
ALLOWLIST = {"SRC-001", "SRC-002", "SRC-003", "SRC-004", "SRC-005"}

# Government domains automatically get benefit of doubt
TRUSTED_GOVERNMENT_DOMAINS = {".gov.br", ".gov"}

# License types that permit full text storage
PERMISSIVE_LICENSES = {
    "public_domain",
    "cc0",
    "cc-by",
    "open_government_license",
    "government_open_data",
}


class PolicyGate:
    """
    Policy gate evaluator for source compliance.

    Determines access level based on:
    - Allowlist membership
    - License type and clarity
    - robots.txt compliance
    - ToS restrictions (if known)
    - PII risk level
    """

    def __init__(self, fail_closed: bool = True, audit_logger: Optional[Callable[..., UUID]] = None):
        """
        Initialize policy gate.

        Args:
            fail_closed: If True, default to METADATA_ONLY on ambiguity (recommended)
        """
        self.fail_closed = fail_closed
        self.audit_logger = audit_logger
        self.logger = logging.getLogger(f"{__name__}.PolicyGate")

    def evaluate(self, source: Any) -> PolicyDecision:
        """
        Evaluate source and return policy decision.

        Args:
            source: Source dict or Source ORM object

        Returns:
            PolicyDecision enum (ALLOW/METADATA_ONLY/BLOCK)
        """
        # Extract source fields (support dict or ORM object)
        source_id, metadata, base_url = self._extract_source_fields(source)

        self.logger.info(f"Evaluating policy for {source_id}")

        # Rule 1: Check allowlist (mandatory)
        if not self._check_allowlist(source_id):
            self.logger.warning(f"{source_id} not in allowlist → BLOCK")
            decision = PolicyDecision.BLOCK
            self._log_decision(source_id, decision, metadata)
            return decision

        # Rule 2: Check robots.txt compliance
        robots_decision = self._check_robots(metadata)
        if robots_decision == PolicyDecision.BLOCK:
            self.logger.warning(f"{source_id} blocked by robots.txt → BLOCK")
            decision = PolicyDecision.BLOCK
            self._log_decision(source_id, decision, metadata)
            return decision

        # Rule 3: Check license
        license_decision = self._check_license(metadata, base_url)
        if license_decision == PolicyDecision.BLOCK:
            self.logger.warning(f"{source_id} license prohibits access → BLOCK")
            decision = PolicyDecision.BLOCK
            self._log_decision(source_id, decision, metadata)
            return decision

        # Rule 4: Check ToS (if available)
        tos_decision = self._check_tos(metadata)
        if tos_decision == PolicyDecision.BLOCK:
            self.logger.warning(f"{source_id} ToS prohibits scraping → BLOCK")
            decision = PolicyDecision.BLOCK
            self._log_decision(source_id, decision, metadata)
            return decision

        # Rule 5: Check PII risk
        pii_decision = self._check_pii(metadata)
        if pii_decision == PolicyDecision.BLOCK:
            self.logger.warning(f"{source_id} PII risk too high → BLOCK")
            decision = PolicyDecision.BLOCK
            self._log_decision(source_id, decision, metadata)
            return decision

        # Aggregate decisions (most restrictive wins)
        decisions = [license_decision, robots_decision, tos_decision, pii_decision]

        if PolicyDecision.METADATA_ONLY in decisions:
            self.logger.info(f"{source_id} → METADATA_ONLY (restrictive condition)")
            decision = PolicyDecision.METADATA_ONLY
            self._log_decision(source_id, decision, metadata)
            return decision

        # All checks passed → ALLOW
        self.logger.info(f"{source_id} → ALLOW (all checks passed)")
        decision = PolicyDecision.ALLOW
        self._log_decision(source_id, decision, metadata)
        return decision

    def _log_decision(self, source_id: str, decision: PolicyDecision, metadata: Dict[str, Any]) -> None:
        """Emit audit log entry for policy decisions (best-effort)."""
        if not self.audit_logger:
            return

        try:
            self.audit_logger(
                event_type="policy_check",
                source_id=source_id,
                action="evaluate",
                details={
                    "decision": decision.value,
                    "license_status": (metadata.get("license_policy") or {}).get("license_status"),
                    "robots_respect": (metadata.get("crawl_policy") or {}).get("robots_respect"),
                },
                actor="policy_gate",
                result="success",
            )
        except Exception as exc:  # pragma: no cover - best-effort logging
            self.logger.warning("Audit logger failed: %s", exc)

    def _extract_source_fields(self, source: Any) -> Tuple[str, Dict[str, Any], Optional[str]]:
        """Extract source_id, metadata, base_url from dict or ORM object."""
        if isinstance(source, dict):
            source_id = source.get("source_id", "unknown")
            metadata = source.get("metadata", {})
            base_url = source.get("url") or source.get("base_url")
        else:
            source_id = getattr(source, "source_id", "unknown")
            metadata = getattr(source, "metadata_", {}) or {}
            base_url = getattr(source, "url", None)

        return source_id, metadata, base_url

    def _check_allowlist(self, source_id: str) -> bool:
        """Check if source is in allowlist."""
        return source_id in ALLOWLIST

    def _check_license(self, metadata: Dict[str, Any], base_url: Optional[str]) -> PolicyDecision:
        """
        Check license compliance.

        Returns:
            ALLOW: Permissive license (public domain, CC0, open gov)
            METADATA_ONLY: License unclear or restrictive
            BLOCK: License explicitly prohibits (rare)
        """
        license_info = metadata.get("license_policy") or metadata.get("license")

        if not license_info:
            # Missing license → fail-closed
            if self.fail_closed:
                # Government domains get benefit of doubt (METADATA_ONLY, not BLOCK)
                if base_url and any(d in base_url for d in TRUSTED_GOVERNMENT_DOMAINS):
                    self.logger.info("Missing license on .gov domain → METADATA_ONLY")
                    return PolicyDecision.METADATA_ONLY
                else:
                    self.logger.warning("Missing license, non-gov domain → METADATA_ONLY")
                    return PolicyDecision.METADATA_ONLY
            else:
                return PolicyDecision.ALLOW

        # Extract license type/status
        if isinstance(license_info, dict):
            license_type = license_info.get("license_type", "").lower()
            license_status = license_info.get("license_status", "unknown").lower()
            storage_mode = license_info.get("default_storage_mode", "").upper()

            # Check explicit storage mode
            if storage_mode == "BLOCK":
                return PolicyDecision.BLOCK
            elif storage_mode == "METADATA_ONLY":
                return PolicyDecision.METADATA_ONLY
            elif storage_mode == "ALLOW":
                return PolicyDecision.ALLOW

            # Check license status
            if license_status == "verified" and license_type in PERMISSIVE_LICENSES:
                return PolicyDecision.ALLOW
            elif license_status == "unknown":
                return PolicyDecision.METADATA_ONLY
            elif license_status == "prohibited":
                return PolicyDecision.BLOCK
            else:
                # Ambiguous → fail-closed
                return PolicyDecision.METADATA_ONLY

        # License is string → check if permissive
        license_str = str(license_info).lower()
        if any(lic in license_str for lic in PERMISSIVE_LICENSES):
            return PolicyDecision.ALLOW
        else:
            return PolicyDecision.METADATA_ONLY

    def _check_robots(self, metadata: Dict[str, Any]) -> PolicyDecision:
        """
        Check robots.txt compliance.

        Returns:
            BLOCK: robots.txt explicitly disallows
            METADATA_ONLY: Strict crawl_delay (>5s)
            ALLOW: robots.txt allows or missing (gov sites)
        """
        crawl_policy = metadata.get("crawl_policy", {})
        robots_respect = crawl_policy.get("robots_respect", True)

        if not robots_respect:
            # Source configured to ignore robots → BLOCK
            return PolicyDecision.BLOCK

        # Check for explicit disallow
        robots_disallow = metadata.get("robots_disallow", False)
        if robots_disallow:
            return PolicyDecision.BLOCK

        # Check crawl delay
        crawl_delay = crawl_policy.get("crawl_delay_s", 0)
        if crawl_delay > 5:
            # Very strict delay suggests reluctance
            self.logger.info(f"High crawl_delay ({crawl_delay}s) → METADATA_ONLY")
            return PolicyDecision.METADATA_ONLY

        # robots.txt allows or missing (typical for gov sites)
        return PolicyDecision.ALLOW

    def _check_tos(self, metadata: Dict[str, Any]) -> PolicyDecision:
        """
        Check Terms of Service restrictions.

        Returns:
            BLOCK: ToS explicitly prohibits scraping
            METADATA_ONLY: ToS ambiguous
            ALLOW: ToS permits or silent (gov sites)
        """
        tos_info = metadata.get("tos") or metadata.get("terms_of_service")

        if not tos_info:
            # No ToS → assume ALLOW (common for gov sites)
            return PolicyDecision.ALLOW

        if isinstance(tos_info, dict):
            tos_status = tos_info.get("scraping_allowed", "unknown").lower()

            if tos_status == "prohibited":
                return PolicyDecision.BLOCK
            elif tos_status == "allowed":
                return PolicyDecision.ALLOW
            else:
                # Ambiguous → fail-closed
                return PolicyDecision.METADATA_ONLY

        # ToS is string → check for prohibition keywords
        tos_str = str(tos_info).lower()
        if any(word in tos_str for word in ["prohibit", "forbidden", "not allowed", "illegal"]):
            return PolicyDecision.BLOCK
        else:
            return PolicyDecision.ALLOW

    def _check_pii(self, metadata: Dict[str, Any]) -> PolicyDecision:
        """
        Check PII risk and mitigation.

        Returns:
            BLOCK: High PII risk without redaction plan
            METADATA_ONLY: Medium PII risk
            ALLOW: Low PII or redaction configured
        """
        data_handling = metadata.get("data_handling", {})
        pii_expected = data_handling.get("pii_expected", "low").lower()
        pii_actions = data_handling.get("pii_actions", [])

        if pii_expected == "high":
            # High PII → require redaction plan
            if "redact" in pii_actions or "anonymize" in pii_actions:
                return PolicyDecision.METADATA_ONLY  # Conservative
            else:
                return PolicyDecision.BLOCK  # No mitigation
        elif pii_expected == "medium":
            # Medium PII → conservative
            return PolicyDecision.METADATA_ONLY
        else:
            # Low or none → allow
            return PolicyDecision.ALLOW
