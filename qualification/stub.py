"""No-op qualification stub for Phase 1 transition scaffolding."""

from __future__ import annotations

from dataclasses import dataclass

from .port import QualificationPort, QualificationResult


@dataclass(frozen=True)
class StubQualificationAdapter(QualificationPort):
    """Placeholder adapter that returns a deterministic undecided result."""

    def qualify(self, matched: bool, attributes: dict[str, int]) -> QualificationResult:
        return QualificationResult(
            label="unknown_activity",
            preliminary=True,
            explanation="phase1_stub",
        )
