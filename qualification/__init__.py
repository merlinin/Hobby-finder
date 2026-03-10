"""Qualification package scaffold for hobby status decisions.

Phase 1 / Slice 5: port + stub prepared without runtime integration.
"""

from .port import QualificationPort, QualificationResult
from .stub import StubQualificationAdapter

__all__ = ["QualificationPort", "QualificationResult", "StubQualificationAdapter"]
