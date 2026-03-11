"""Stub adapter for personal status."""

from __future__ import annotations

from dataclasses import dataclass

from qualification.port import QualificationStatus

from .port import PersonalStatusResult, UserContext


@dataclass(frozen=True)
class StubPersonalStatusAdapter:
    """Simple stub that always returns not_a_hobby."""

    def derive(self, qualification_status: QualificationStatus, context: UserContext) -> PersonalStatusResult:
        return PersonalStatusResult(
            status="not_a_hobby",
            explanation="Stub-Bewertung: keine persönliche Kontextlogik aktiv.",
        )
