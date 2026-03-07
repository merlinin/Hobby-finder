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

STOPWORDS = {
    # German function words
    "und", "oder", "der", "die", "das", "ein", "eine", "einer", "eines", "einem", "einen",
    "ist", "sind", "im", "in", "mit", "von", "für", "auf", "als", "auch", "zu", "den", "dem",
    "des", "bei", "dass", "es", "sie", "er", "man", "wir", "ihr", "ihre", "seine", "sein",
    "wird", "werden", "kann", "können", "unter", "sowie", "jedoch", "diese", "dieser", "dieses", "zur", "aus", "nicht",
    # English function words
    "the", "a", "an", "and", "or", "is", "are", "to", "of", "in", "on", "for", "with", "by",
    # Noise words from definitions/links
    "working", "free", "time", "neben", "one", "especially", "link", "https", "http", "text",
    "wikipedia", "dictionary", "duden", "cambridge", "oxford", "merriam", "webster",
    # Generic, non-content terms
    "hobby", "hobbys", "begriff", "quelle", "quellen", "definition", "definitionen",
}

NORMALIZATION_MAP = {
    "ausübt": "ausüben",
    "ausgeübt": "ausüben",
    "auszuüben": "ausüben",
    "freiwillige": "freiwillig",
    "freiwilligen": "freiwillig",
    "regelmäßige": "regelmäßig",
    "regelmäßigen": "regelmäßig",
    "regelmässig": "regelmäßig",
    "beschaeftigung": "beschäftigung",
    "beschäftigungen": "beschäftigung",
    "taetigkeit": "tätigkeit",
    "taetigkeiten": "tätigkeit",
    "interessen": "interesse",
    "neigungen": "neigung",
    "leidenschaften": "leidenschaft",
    "sammlung": "sammeln",
    "sammelns": "sammeln",
    "lernens": "lernen",
}

WORD_CATEGORIES = {
    "handlung": {"tätigkeit", "beschäftigung", "ausüben", "lernen", "sammeln", "kreativ", "sport"},
    "motivation": {"interesse", "neigung", "leidenschaft"},
    "emotion": {"freude", "entspannung"},
    "rahmen": {"freizeit", "freiwillig", "regelmäßig"},
}

CATEGORY_COLORS = {
    "handlung": "#2f6fed",
    "motivation": "#2e8b57",
    "emotion": "#f08c00",
    "rahmen": "#6c757d",
    "default": "#4c5a73",
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


def _normalize_word(word: str) -> str:
    normalized = word.lower().strip()
    normalized = normalized.replace("ae", "ä").replace("oe", "ö").replace("ue", "ü")
    return NORMALIZATION_MAP.get(normalized, normalized)


def _word_color(word: str, **_: object) -> str:
    normalized = _normalize_word(word)
    for category, words in WORD_CATEGORIES.items():
        if normalized in words:
            return CATEGORY_COLORS[category]
    return CATEGORY_COLORS["default"]


def get_top_words(top_n: int = 20) -> list[tuple[str, int]]:
    """Return the most frequent words from the definitions text."""
    normalized = _normalize_text(_load_source_text())
    words = []
    for raw_word in normalized.split():
        word = _normalize_word(raw_word)
        if len(word) <= 2:
            continue
        if word in STOPWORDS:
            continue
        words.append(word)
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
        color_func=_word_color,
    ).generate_from_frequencies(frequencies)
    return cloud.to_image()
