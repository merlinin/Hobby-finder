"""Contracts for the preliminary qualification endpoint (Phase 2 Slice 1)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualificationInput:
    """Minimal request DTO for /qualify."""

    activity: str
