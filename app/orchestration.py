"""Thin application orchestration layer for phase-1 transition.

This module introduces a minimal composition boundary without changing runtime
behavior. It delegates directly to existing adapters/services.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from research.adapter import ResearchAdapter


@dataclass
class AppOrchestrator:
    """Pass-through facade used by Flask routes during the transition phase."""

    research_adapter: ResearchAdapter = field(default_factory=ResearchAdapter)

    def get_index_context(self) -> dict[str, object]:
        """Return template context for the landing page."""
        return {"top_words": self.research_adapter.get_top_words(top_n=12)}

    def generate_wordcloud_image(self):
        """Return the wordcloud image from the research adapter unchanged."""
        return self.research_adapter.generate_wordcloud_image()
