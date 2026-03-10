"""Port definitions for hobby qualification."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol


QualificationStatus = Literal[
    "qualified_hobby",
    "potential_hobby",
    "insufficient_evidence",
    "unlikely_hobby",
]
SupportStrength = Literal["strong", "moderate", "limited", "weak"]


@dataclass(frozen=True)
class QualificationResult:
    """Explainable qualification result based on deterministic rules."""

    status: QualificationStatus
    preliminary: bool
    score: float
    support_strength: SupportStrength
    supporting_attributes: list[str]
    missing_or_weak_attributes: list[str]
    explanation: str


class QualificationPort(Protocol):
    """Contract for explainable and deterministic qualification."""

    def qualify(self, matched: bool, attributes: dict[str, int]) -> QualificationResult:
        """Return explainable qualification from match state and activity attributes."""
