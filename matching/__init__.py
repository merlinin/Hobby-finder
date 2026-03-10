"""Matching package scaffold for text-to-activity mapping.

Phase 1 / Slice 5: port + stub prepared without runtime integration.
"""

from .port import MatchResult, MatchingPort
from .stub import StubMatchingAdapter

__all__ = ["MatchResult", "MatchingPort", "StubMatchingAdapter"]
