"""No-op qualification stub for transition scaffolding."""

from __future__ import annotations

from dataclasses import dataclass

from .port import QualificationPort, QualificationResult


@dataclass(frozen=True)
class StubQualificationAdapter(QualificationPort):
    """Placeholder adapter that returns a deterministic undecided result."""

    def qualify(self, matched: bool, attributes: dict[str, int]) -> QualificationResult:
        return QualificationResult(
            status="insufficient_evidence",
            preliminary=True,
            score=0.0,
            support_strength="weak",
            supporting_attributes=[],
            missing_or_weak_attributes=["freiwillig", "freizeit", "regelmäßig"],
            explanation="phase_stub: no qualification logic attached",
        )
