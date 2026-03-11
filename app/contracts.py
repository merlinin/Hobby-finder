"""Contracts for the qualification endpoint."""

from __future__ import annotations

from dataclasses import dataclass

from personal_status.port import Frequency, PersonalImportance


@dataclass(frozen=True)
class QualificationInput:
    """Request DTO for /qualify with optional personal context."""

    activity: str
    currently_active: bool | None = None
    previously_active: bool | None = None
    frequency: Frequency | None = None
    personal_importance: PersonalImportance | None = None
    intends_to_resume: bool | None = None
