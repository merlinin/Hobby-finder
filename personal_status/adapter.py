"""Deterministic personal status adapter."""

from __future__ import annotations

from dataclasses import dataclass

from qualification.port import QualificationStatus

from .port import PersonalStatusPort, PersonalStatusResult, UserContext

POSITIVE_QUALIFICATION: set[QualificationStatus] = {"qualified_hobby", "potential_hobby"}
NON_POSITIVE_QUALIFICATION: set[QualificationStatus] = {"insufficient_evidence", "unlikely_hobby"}


@dataclass(frozen=True)
class PersonalStatusAdapter(PersonalStatusPort):
    """Derive a personal hobby status from qualification and optional user context."""

    def derive(self, qualification_status: QualificationStatus, context: UserContext) -> PersonalStatusResult:
        currently_active = context.currently_active
        previously_active = context.previously_active
        intends_to_resume = context.intends_to_resume
        frequency = context.frequency
        importance = context.personal_importance

        regular_enough = frequency in {"occasionally", "regularly"}
        meaningful = importance in {"medium", "high"}

        if currently_active is False and previously_active is True and intends_to_resume is True:
            return PersonalStatusResult(
                status="dormant_hobby",
                explanation=(
                    "Du warst mit der Aktivität früher aktiv, bist aktuell pausiert und möchtest wieder "
                    "einsteigen; deshalb wird sie als dormant_hobby eingeordnet."
                ),
            )

        if currently_active is False and previously_active is True and intends_to_resume is False:
            return PersonalStatusResult(
                status="former_hobby",
                explanation=(
                    "Du warst mit der Aktivität früher aktiv, bist aktuell nicht aktiv und planst keine "
                    "Wiederaufnahme; deshalb former_hobby."
                ),
            )

        if (
            currently_active is True
            and regular_enough
            and meaningful
            and qualification_status in POSITIVE_QUALIFICATION
        ):
            return PersonalStatusResult(
                status="active_hobby",
                explanation=(
                    "Die Aktivität ist grundsätzlich hobbytypisch. Da du sie aktuell mit gewisser "
                    "Regelmäßigkeit ausübst und sie dir wichtig ist, wird sie als active_hobby bewertet."
                ),
            )

        if self._is_emerging_interest(qualification_status, context):
            return PersonalStatusResult(
                status="emerging_interest",
                explanation=(
                    "Es gibt erkennbare positive Signale (z. B. erste Aktivität, Interesse oder "
                    "Wiederaufnahmeabsicht), aber noch kein stabiles Muster für ein aktives Hobby; "
                    "daher emerging_interest."
                ),
            )

        if self._has_sufficient_negative_evidence(qualification_status, context):
            return PersonalStatusResult(
                status="not_a_hobby",
                explanation=(
                    "Die Aktivität ist aktuell eher kein Hobby: Die allgemeine Einordnung ist nicht "
                    "hobbytypisch und die persönlichen Angaben sprechen ebenfalls klar dagegen."
                ),
            )

        return PersonalStatusResult(
            status="insufficient_personal_context",
            explanation=(
                "Für eine belastbare persönliche Einordnung fehlen ausreichende Angaben. Das ist keine "
                "Aussage, dass die Aktivität kein Hobby ist."
            ),
        )

    def _is_emerging_interest(self, qualification_status: QualificationStatus, context: UserContext) -> bool:
        positive_qualification = qualification_status in POSITIVE_QUALIFICATION

        return (
            (context.currently_active is True and context.frequency == "rarely" and positive_qualification)
            or (context.currently_active is True and context.personal_importance in {"medium", "high"} and positive_qualification)
            or (context.intends_to_resume is True and context.previously_active is not True)
            or (context.personal_importance in {"medium", "high"} and context.currently_active is None and positive_qualification)
        )

    def _has_sufficient_negative_evidence(
        self,
        qualification_status: QualificationStatus,
        context: UserContext,
    ) -> bool:
        if qualification_status not in NON_POSITIVE_QUALIFICATION:
            return False

        negative_signals = 0
        if context.currently_active is False:
            negative_signals += 1
        if context.previously_active is False:
            negative_signals += 1
        if context.intends_to_resume is False:
            negative_signals += 1
        if context.personal_importance == "low":
            negative_signals += 1
        if context.frequency == "rarely":
            negative_signals += 1

        return negative_signals >= 3
