"""filler_word_detector: deterministic (non-LLM) scan for common filler
words/hedging phrases in an answer.
"""

import re

_FILLER_PATTERNS = [
    r"\bum\b",
    r"\buh\b",
    r"\blike\b",
    r"\bkind of\b",
    r"\bsort of\b",
    r"\bi guess\b",
    r"\bi think maybe\b",
    r"\bbasically\b",
    r"\bactually\b",
    r"\bjust\b",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _FILLER_PATTERNS]


def detect_filler_words(answer: str) -> list[str]:
    """Return the distinct filler phrases found in the answer, if any."""
    found = set()
    for pattern in _COMPILED:
        if pattern.search(answer):
            found.add(pattern.pattern.strip(r"\b").replace("\\", ""))
    return sorted(found)