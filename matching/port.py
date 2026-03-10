"""Port definitions for future activity-matching integration.

Phase 1 / Slice 5: structural contract only, no runtime wiring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class MatchResult:
    """Minimal matching result shape for future phases."""

    activity_name: str | None
    confidence: float


class MatchingPort(Protocol):
    """Contract for mapping free-text activity input to a canonical activity."""

    def match_activity(self, activity_text: str) -> MatchResult:
        """Return a canonical activity candidate plus confidence metadata."""
