"""Port definitions for future hobby-qualification integration.

Phase 1 / Slice 5: structural contract only, no runtime wiring.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class QualificationResult:
    """Minimal qualification result shape for future phases."""

    status: str
    rationale: str


class QualificationPort(Protocol):
    """Contract for classifying whether an activity qualifies as a hobby."""

    def qualify(self, activity_name: str, user_context: dict[str, object]) -> QualificationResult:
        """Return hobby-status decision metadata for an activity and user context."""
