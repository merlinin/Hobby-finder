"""Transition adapter for research-related read-only operations.

Phase 1 / Slice 2:
- expose stable adapter methods for existing wordcloud/definition-analysis behavior
- delegate directly to legacy implementation without transforming outputs
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import wordcloud_service


@dataclass(frozen=True)
class ResearchAdapter:
    """Read-only adapter over the current research implementation."""

    get_top_words_fn: Callable[[int], list[tuple[str, int]]] = wordcloud_service.get_top_words
    generate_wordcloud_image_fn: Callable[[], object] = wordcloud_service.generate_wordcloud_image

    def get_top_words(self, top_n: int = 20) -> list[tuple[str, int]]:
        """Delegate to legacy top-word extraction without changing behavior."""
        return self.get_top_words_fn(top_n=top_n)

    def generate_wordcloud_image(self):
        """Delegate to legacy wordcloud image generation without changing behavior."""
        return self.generate_wordcloud_image_fn()
