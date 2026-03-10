"""Minimal production matching adapter for Phase 2 Slice 1."""

from __future__ import annotations

from dataclasses import dataclass, field

from .port import MatchResult, MatchingPort


def _normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


@dataclass(frozen=True)
class MatchingAdapter(MatchingPort):
    """Exact-name and exact-alias matcher with transparent scoring."""

    alias_map: dict[str, str] = field(
        default_factory=lambda: {
            "bouldern": "Klettern",
            "mountainbike": "Radfahren",
            "mountainbiken": "Radfahren",
            "gitarre": "Gitarre spielen",
            "musik machen": "Musik machen",
            "3d druck": "3D-Druck",
            "3d-druck": "3D-Druck",
            "zeichnen": "Zeichnen",
            "kunst": "Zeichnen",
            "autos reparieren": "Autos reparieren",
            "autoschrauben": "Autos reparieren",
            "gaertnern": "Gärtnern",
        }
    )

    def match_activity(self, activity_text: str, canonical_names: list[str]) -> MatchResult:
        normalized_input = _normalize(activity_text)
        normalized_names = {_normalize(name): name for name in canonical_names}

        if normalized_input in normalized_names:
            return MatchResult(
                matched=True,
                activity_name=normalized_names[normalized_input],
                match_type="exact_name",
                confidence=1.0,
            )

        if normalized_input in self.alias_map:
            return MatchResult(
                matched=True,
                activity_name=self.alias_map[normalized_input],
                match_type="exact_alias",
                confidence=0.9,
            )

        return MatchResult(
            matched=False,
            activity_name=None,
            match_type="none",
            confidence=0.0,
        )
