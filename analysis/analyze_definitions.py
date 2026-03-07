"""Analyze hobby definitions and optionally generate a word cloud PNG."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

DEFAULT_INPUT = Path("data/definitions.json")
DEFAULT_OUTPUT = Path("analysis/artifacts/wordcloud.png")

BASE_STOPWORDS = {
    "und", "oder", "der", "die", "das", "ein", "eine", "einer", "eines", "einem", "einen",
    "ist", "sind", "im", "in", "mit", "von", "für", "auf", "als", "auch", "zu", "den", "dem",
    "des", "bei", "dass", "es", "sie", "er", "man", "wir", "ihr", "ihre", "seine", "sein",
    "the", "a", "an", "and", "or", "is", "are", "to", "of", "in", "on", "for", "with", "by",
    "hobby", "hobbys", "working", "free", "time", "one", "especially", "link", "https", "http", "zur", "aus", "nicht",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--top-n", type=int, default=10)
    parser.add_argument("--domain-stopwords", type=str, default="")
    parser.add_argument("--skip-wordcloud", action="store_true")
    return parser.parse_args()


def load_records(path: Path) -> list[dict[str, str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("definitions.json must contain a JSON array")
    return [item for item in data if isinstance(item, dict)]


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"[^\wäöüß]+", " ", text)
    return text


def tokenize(text: str, stopwords: set[str]) -> list[str]:
    tokens = []
    for token in normalize_text(text).split():
        if len(token) <= 2 or token in stopwords:
            continue
        tokens.append(token)
    return tokens


def build_stopwords(domain_stopwords: str) -> set[str]:
    extra = {w.strip().lower() for w in domain_stopwords.split(",") if w.strip()}
    return BASE_STOPWORDS | extra


def save_wordcloud(freqs: dict[str, int], output: Path) -> None:
    try:
        from wordcloud import WordCloud
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError(
            "wordcloud package is not installed. Install requirements or run with --skip-wordcloud."
        ) from exc

    output.parent.mkdir(parents=True, exist_ok=True)
    WordCloud(width=1200, height=600, background_color="white").generate_from_frequencies(freqs).to_file(str(output))


def main() -> int:
    args = parse_args()
    records = load_records(args.input)
    combined_text = "\n".join(str(item.get("text", "")) for item in records)

    stopwords = build_stopwords(args.domain_stopwords)
    frequencies = Counter(tokenize(combined_text, stopwords))

    if not args.skip_wordcloud and frequencies:
        save_wordcloud(dict(frequencies), args.output)
        print(f"Word cloud saved to: {args.output}")

    print(f"Top {args.top_n} most frequent words in definitions:")
    for word, count in frequencies.most_common(args.top_n):
        print(f"{word}: {count}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
