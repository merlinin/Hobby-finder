"""Minimal production matching adapter for Phase 2 Slice 1."""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .port import MatchResult, MatchingPort


_SIMPLE_PHRASE_SIMPLIFICATIONS = {
    "klettern gehen": "klettern",
    "musik machen": "musik",
    "fahrrad fahren": "fahrrad",
}


def _normalize(text: str) -> str:
    normalized = text.strip().lower()
    normalized = normalized.replace("-", " ")
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    normalized = " ".join(normalized.split())
    return normalized


def _simplify_phrase(normalized_text: str) -> str:
    return _SIMPLE_PHRASE_SIMPLIFICATIONS.get(normalized_text, normalized_text)


@dataclass(frozen=True)
class MatchingAdapter(MatchingPort):
    """Exact-name and exact-alias matcher with transparent scoring."""

    alias_map: dict[str, str] = field(
        default_factory=lambda: {
            "bouldern": "Klettern",
            "mountainbike": "Radfahren",
            "mountainbiken": "Radfahren",
            "gitarre": "Gitarre spielen",
            "musik": "Musik machen",
            "musik machen": "Musik machen",
            "3d druck": "3D-Druck",
            "zeichnen": "Zeichnen",
            "kunst": "Zeichnen",
            "autos reparieren": "Autos reparieren",
            "autoschrauben": "Autos reparieren",
            "gaertnern": "Gärtnern",
            "fahrrad": "Radfahren",
        }
    )

    def match_activity(self, activity_text: str, canonical_names: list[str]) -> MatchResult:
        normalized_input = _normalize(activity_text)
        normalized_names = {_normalize(name): name for name in canonical_names}
        normalized_alias_map = {_normalize(alias): target for alias, target in self.alias_map.items()}

        direct_match = self._match_by_key(normalized_input, normalized_names, normalized_alias_map)
        if direct_match is not None:
            return direct_match

        simplified_input = _simplify_phrase(normalized_input)
        if simplified_input != normalized_input:
            simplified_match = self._match_by_key(simplified_input, normalized_names, normalized_alias_map)
            if simplified_match is not None:
                return simplified_match

        return MatchResult(
            matched=False,
            activity_name=None,
            match_type="none",
            confidence=0.0,
        )

    def _match_by_key(
        self,
        normalized_input: str,
        normalized_names: dict[str, str],
        normalized_alias_map: dict[str, str],
    ) -> MatchResult | None:
        if normalized_input in normalized_names:
            return MatchResult(
                matched=True,
                activity_name=normalized_names[normalized_input],
                match_type="exact_name",
                confidence=1.0,
            )

        if normalized_input in normalized_alias_map:
            return MatchResult(
                matched=True,
                activity_name=normalized_alias_map[normalized_input],
                match_type="exact_alias",
                confidence=0.9,
            )

        return None
