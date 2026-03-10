"""No-op qualification stub for Phase 1 transition scaffolding.

This is intentionally not wired into app runtime behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from .port import QualificationPort, QualificationResult


@dataclass(frozen=True)
class StubQualificationAdapter(QualificationPort):
    """Placeholder adapter that returns a deterministic undecided result."""

    def qualify(self, activity_name: str, user_context: dict[str, object]) -> QualificationResult:
        return QualificationResult(status="unqualified", rationale="phase1_stub")
