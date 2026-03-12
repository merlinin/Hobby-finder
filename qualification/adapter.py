"""Production qualification adapter with transparent, deterministic rules."""

from __future__ import annotations

from dataclasses import dataclass

from .port import QualificationPort, QualificationResult, QualificationStatus, SupportStrength

CORE_ATTRIBUTES = ("freiwillig", "freizeit", "regelmäßig")


@dataclass(frozen=True)
class PreliminaryQualificationAdapter(QualificationPort):
    """Deterministic, transparent rules for preliminary qualification."""

    def qualify(self, matched: bool, attributes: dict[str, int]) -> QualificationResult:
        normalized_attributes = {name.lower(): value for name, value in attributes.items()}

        if not matched:
            return self._build_result(
                status="insufficient_evidence",
                score=0.0,
                supporting_attributes=[],
                missing_or_weak_attributes=list(CORE_ATTRIBUTES),
                reason=(
                    "Die Aktivität konnte nicht zuverlässig zugeordnet werden; ohne eindeutigen Treffer "
                    "ist aktuell keine belastbare Hobby-Einschätzung möglich."
                ),
            )

        if not normalized_attributes:
            return self._build_result(
                status="insufficient_evidence",
                score=0.0,
                supporting_attributes=[],
                missing_or_weak_attributes=list(CORE_ATTRIBUTES),
                reason=(
                    "Die Aktivität wurde erkannt, aber es liegen keine Attributdaten vor. "
                    "Darum bleibt die Einstufung vorläufig und evidenzschwach."
                ),
            )

        core_present = sum(1 for attr in CORE_ATTRIBUTES if attr in normalized_attributes)
        strong_core = sum(1 for attr in CORE_ATTRIBUTES if normalized_attributes.get(attr, 0) >= 2)

        supporting_attributes = [
            f"{name} ({value})"
            for name, value in normalized_attributes.items()
            if value >= 2
        ]
        missing_or_weak = [
            f"{attr} ({normalized_attributes.get(attr, 0)})" if attr in normalized_attributes else f"{attr} (fehlt)"
            for attr in CORE_ATTRIBUTES
            if normalized_attributes.get(attr, 0) < 2
        ]

        max_points = len(CORE_ATTRIBUTES) * 2 + max(0, len(normalized_attributes) - len(CORE_ATTRIBUTES))
        achieved_points = 0
        for attr in CORE_ATTRIBUTES:
            value = normalized_attributes.get(attr, 0)
            achieved_points += 2 if value >= 2 else 1 if value == 1 else 0
        achieved_points += sum(
            1
            for name, value in normalized_attributes.items()
            if name not in CORE_ATTRIBUTES and value >= 2
        )
        score = round(achieved_points / max_points if max_points else 0.0, 2)

        if core_present < 2:
            status: QualificationStatus = "insufficient_evidence"
            reason = "Zu wenige Kernattribute sind belegt, daher reicht die Evidenz nicht für eine klare Einordnung."
        elif strong_core >= 2 and score >= 0.6:
            status = "qualified_hobby"
            reason = "Mehrere Kernattribute sind deutlich erfüllt; die Aktivität zeigt ein klares Hobby-Profil."
        elif strong_core == 0:
            status = "unlikely_hobby"
            reason = "Kernattribute sind zwar vorhanden, aber durchgehend schwach ausgeprägt; damit ist Hobby-Qualifikation derzeit unwahrscheinlich."
        elif strong_core >= 1 and score >= 0.4:
            status = "potential_hobby"
            reason = "Ein Teil der Kernattribute spricht für ein Hobby, aber die Evidenz ist noch uneinheitlich."
        else:
            status = "insufficient_evidence"
            reason = "Die vorhandenen Merkmale erlauben aktuell keine robuste Einordnung."

        return self._build_result(
            status=status,
            score=score,
            supporting_attributes=supporting_attributes,
            missing_or_weak_attributes=missing_or_weak,
            reason=reason,
        )

    def _build_result(
        self,
        status: QualificationStatus,
        score: float,
        supporting_attributes: list[str],
        missing_or_weak_attributes: list[str],
        reason: str,
    ) -> QualificationResult:
        strength: SupportStrength
        if score >= 0.75:
            strength = "strong"
        elif score >= 0.5:
            strength = "moderate"
        elif score >= 0.25:
            strength = "limited"
        else:
            strength = "weak"

        explanation = (
            f"Allgemeine Einschätzung der Tätigkeit: {status}. "
            f"Dafür sprechen: {', '.join(supporting_attributes) if supporting_attributes else 'keine klar starken Merkmale'}. "
            f"Unsicher oder schwach: {', '.join(missing_or_weak_attributes) if missing_or_weak_attributes else 'keine auffälligen Schwächen'}. "
            f"Einordnung: {reason}"
        )

        return QualificationResult(
            status=status,
            preliminary=True,
            score=score,
            support_strength=strength,
            supporting_attributes=supporting_attributes,
            missing_or_weak_attributes=missing_or_weak_attributes,
            explanation=explanation,
        )
