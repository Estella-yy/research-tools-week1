"""Count word frequencies in a text file and print the top 10 words."""

import argparse
import re
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[a-z0-9']+")


def count_words(text):
    """Return a Counter mapping each lower-case word to its number of occurrences."""
    return Counter(WORD_RE.findall(text.lower()))


def top_words(counter, limit=10):
    """Return the `limit` most common words as (word, count) pairs."""
    return counter.most_common(limit)


def format_report(pairs):
    """Render (word, count) pairs as an aligned, numbered list."""
    lines = [f"{rank:>2}. {word:<12} {count}" for rank, (word, count) in enumerate(pairs, 1)]
    return "\n".join(lines)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).with_name("sample.txt"),
        help="text file to analyze (default: sample.txt next to this script)",
    )
    parser.add_argument("-n", "--top", type=int, default=10, help="how many words to show (default: 10)")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    if not args.path.is_file():
        raise SystemExit(f"error: file not found: {args.path}")

    counter = count_words(args.path.read_text(encoding="utf-8"))
    if not counter:
        print(f"no words found in {args.path}")
        return 0

    print(f"file: {args.path}")
    print(f"total words: {sum(counter.values())}, unique words: {len(counter)}")
    print(f"\ntop {args.top} words:\n")
    print(format_report(top_words(counter, args.top)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
