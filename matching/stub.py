"""No-op matching stub for Phase 1 transition scaffolding.

This is intentionally not wired into app runtime behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from .port import MatchResult, MatchingPort


@dataclass(frozen=True)
class StubMatchingAdapter(MatchingPort):
    """Placeholder adapter that returns a deterministic non-match result."""

    def match_activity(self, activity_text: str) -> MatchResult:
        return MatchResult(activity_name=None, confidence=0.0)
