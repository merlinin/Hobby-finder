"""Minimal production qualification adapter for Phase 2 Slice 1."""

from __future__ import annotations

from dataclasses import dataclass

from .port import QualificationPort, QualificationResult


@dataclass(frozen=True)
class PreliminaryQualificationAdapter(QualificationPort):
    """Deterministic, transparent rules for preliminary qualification."""

    def qualify(self, matched: bool, attributes: dict[str, int]) -> QualificationResult:
        if not matched:
            return QualificationResult(
                label="unknown_activity",
                preliminary=True,
                explanation="Die eingegebene Aktivität konnte der Wissensbasis noch nicht eindeutig zugeordnet werden. Das Ergebnis bleibt daher vorläufig und ist keine persönliche Hobby-Bewertung.",
            )

        if not attributes:
            return QualificationResult(
                label="known_activity",
                preliminary=True,
                explanation=(
                    "Die Aktivität wurde erkannt. Aktuell sind dafür jedoch noch keine typischen Eigenschaften hinterlegt, daher ist die Einschätzung nur vorläufig und keine persönliche Hobby-Bewertung."
                ),
            )

        return QualificationResult(
            label="potential_hobby_candidate",
            preliminary=True,
            explanation=(
                "Die Aktivität wurde erkannt und besitzt mehrere typische Eigenschaften eines Hobbys. "
                "Die Einschätzung ist vorläufig und ersetzt keine persönliche Hobby-Bewertung."
            ),
        )
