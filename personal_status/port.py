"""Port definitions for deriving a personal hobby status."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol

from qualification.port import QualificationStatus

Frequency = Literal["rarely", "occasionally", "regularly"]
PersonalImportance = Literal["low", "medium", "high"]

PersonalStatus = Literal[
    "active_hobby",
    "dormant_hobby",
    "former_hobby",
    "emerging_interest",
    "not_a_hobby",
    "insufficient_personal_context",
]


@dataclass(frozen=True)
class UserContext:
    """Optional user-specific context for personal status derivation."""

    currently_active: bool | None = None
    previously_active: bool | None = None
    frequency: Frequency | None = None
    personal_importance: PersonalImportance | None = None
    intends_to_resume: bool | None = None


@dataclass(frozen=True)
class PersonalStatusResult:
    """Explainable, deterministic personal hobby-status output."""

    status: PersonalStatus
    explanation: str


class PersonalStatusPort(Protocol):
    """Contract for combining general qualification with user context."""

    def derive(self, qualification_status: QualificationStatus, context: UserContext) -> PersonalStatusResult:
        """Return personal hobby status and explanation."""
