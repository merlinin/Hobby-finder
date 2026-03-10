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
                explanation="Die Aktivität konnte in der Knowledge Base nicht erkannt werden.",
            )

        if not attributes:
            return QualificationResult(
                label="known_activity",
                preliminary=True,
                explanation=(
                    "Die Aktivität wurde erkannt, es sind aber aktuell keine Attribute hinterlegt."
                ),
            )

        return QualificationResult(
            label="potential_hobby_candidate",
            preliminary=True,
            explanation=(
                "Die Aktivität wurde erkannt und Attribute wurden geladen. "
                "Dies ist eine vorläufige, nicht finale Hobby-Einordnung."
            ),
        )
