"""Port definitions for activity matching."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


MatchType = Literal["exact_match", "alias_match", "normalized_match", "no_match"]


@dataclass(frozen=True)
class MatchResult:
    """Result of matching raw user input to a known canonical activity."""

    matched: bool
    activity_name: str | None
    match_type: MatchType
    normalized_input: str
    confidence: float


class MatchingPort(Protocol):
    """Contract for mapping free-text activity input to a canonical activity."""

    def match_activity(self, activity_text: str, canonical_names: list[str]) -> MatchResult:
        """Return canonical activity match metadata for the user input."""
