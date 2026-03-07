"""Utilities for generating a word cloud from hobby definitions."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

from wordcloud import WordCloud

BASE_DIR = Path(__file__).resolve().parent
DEFINITIONS_PATH = BASE_DIR / "Hobby-Definitionen.txt"

# Deliberately compact starter list; can be extended over time.
STOPWORDS = {
    "und", "oder", "der", "die", "das", "ein", "eine", "einer", "eines", "einem", "einen",
    "ist", "sind", "im", "in", "mit", "von", "für", "auf", "als", "auch", "zu", "den", "dem",
    "des", "bei", "dass", "es", "sie", "er", "man", "wir", "ihr", "ihre", "seine", "sein",
    "hobby", "hobbys", "freizeit", "tätigkeit", "aktivität", "begriff", "link", "https", "http",
    "the", "a", "an", "and", "or", "is", "are", "to", "of", "in", "on", "for", "with", "by",
}


def _load_source_text() -> str:
    if not DEFINITIONS_PATH.exists():
        return ""
    return DEFINITIONS_PATH.read_text(encoding="utf-8")


def _normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\wäöüß]+", " ", text)
    return text


def get_top_words(top_n: int = 20) -> list[tuple[str, int]]:
    """Return the most frequent words from the definitions text."""
    normalized = _normalize_text(_load_source_text())
    words = [word for word in normalized.split() if len(word) > 2 and word not in STOPWORDS]
    return Counter(words).most_common(top_n)


def generate_wordcloud_image():
    """Create a PIL image with the current word cloud."""
    frequencies = dict(get_top_words(top_n=200))
    if not frequencies:
        frequencies = {"hobby": 1}

    cloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        colormap="viridis",
    ).generate_from_frequencies(frequencies)
    return cloud.to_image()
