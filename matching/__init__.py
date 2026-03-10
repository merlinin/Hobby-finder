"""Matching package for text-to-activity mapping."""

from .adapter import MatchingAdapter
from .port import MatchResult, MatchingPort
from .stub import StubMatchingAdapter

__all__ = ["MatchingAdapter", "MatchResult", "MatchingPort", "StubMatchingAdapter"]
