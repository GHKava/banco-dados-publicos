"""
Initialize bots module.
"""

# Lazy imports to avoid SQLAlchemy Python 3.14 issues at import time
from src.bots.robots_checker import RobotsChecker, RobotsCheckResult
from src.bots.validators import get_source_policy_level, validate_source_policy

__all__ = [
    "RobotsChecker",
    "RobotsCheckResult",
    "validate_source_policy",
    "get_source_policy_level",
]
