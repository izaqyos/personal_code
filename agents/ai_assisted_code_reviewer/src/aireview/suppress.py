"""In-code suppressions: `review-ignore RULE-ID: reason` on the line or the line above."""

from __future__ import annotations

import re

SUPPRESS_RE = re.compile(r"review-ignore\s+([A-Z]{2,6}-\d{3}|general)\s*(?::|-|—)?\s*(.*)$")
MIN_REASON = 3


def parse_suppression(line: str) -> tuple[str, str] | None:
    m = SUPPRESS_RE.search(line)
    if not m:
        return None
    reason = m.group(2).strip().rstrip("*/").strip()
    return m.group(1), reason


def is_suppressed(
    rule: str, line: int, file_text: str | None, added_lines: dict[int, str]
) -> str | None:
    """Return the reason if `rule` is suppressed at `line`, else None.

    A suppression without a reason is ignored on purpose: it should be a decision,
    not a mute button.
    """
    lines = file_text.splitlines() if file_text is not None else None

    def lookup(n: int) -> str | None:
        if lines is None:
            return added_lines.get(n)
        return lines[n - 1] if 1 <= n <= len(lines) else None

    for n in (line, line - 1):
        text = lookup(n)
        if not text:
            continue
        parsed = parse_suppression(text)
        if parsed and parsed[0] == rule and len(parsed[1]) >= MIN_REASON:
            return parsed[1]
    return None
