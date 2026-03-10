"""Port definitions for activity matching."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


MatchType = Literal["exact_name", "exact_alias", "none"]


@dataclass(frozen=True)
class MatchResult:
    """Result of matching raw user input to a known canonical activity."""

    matched: bool
    activity_name: str | None
    match_type: MatchType
    confidence: float


class MatchingPort(Protocol):
    """Contract for mapping free-text activity input to a canonical activity."""

    def match_activity(self, activity_text: str, canonical_names: list[str]) -> MatchResult:
        """Return canonical activity match metadata for the user input."""
