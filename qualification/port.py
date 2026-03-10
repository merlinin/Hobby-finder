"""Port definitions for preliminary hobby qualification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


QualificationLabel = Literal[
    "known_activity",
    "unknown_activity",
    "potential_hobby_candidate",
]


@dataclass(frozen=True)
class QualificationResult:
    """Preliminary and explainable qualification result."""

    label: QualificationLabel
    preliminary: bool
    explanation: str


class QualificationPort(Protocol):
    """Contract for preliminary qualification in Slice 1."""

    def qualify(self, matched: bool, attributes: dict[str, int]) -> QualificationResult:
        """Return preliminary result based on match and attribute availability."""
