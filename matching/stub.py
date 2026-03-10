"""No-op matching stub for Phase 1 transition scaffolding."""

from __future__ import annotations

from dataclasses import dataclass

from .port import MatchResult, MatchingPort


@dataclass(frozen=True)
class StubMatchingAdapter(MatchingPort):
    """Placeholder adapter that returns a deterministic non-match result."""

    def match_activity(self, activity_text: str, canonical_names: list[str]) -> MatchResult:
        return MatchResult(matched=False, activity_name=None, match_type="none", confidence=0.0)
