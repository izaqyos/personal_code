"""Repo-level configuration in .ai-review/config.json, merged over defaults."""

from __future__ import annotations

import copy
import json
from pathlib import Path

AI_DIR = ".ai-review"

DEFAULTS: dict = {
    "base": "origin/main",
    "gate": "advisory",  # advisory | blocker
    "override_label": "ai-review-override",
    "min_confidence": 0.6,
    "max_findings": 15,
    "max_diff_chars": 150_000,
    "max_pr_lines": 600,
    "source_globs": ["src/**"],
    "test_globs": [
        "tests/**",
        "test/**",
        "**/*.test.*",
        "**/*.spec.*",
        "**/__tests__/**",
    ],
    "ignore_globs": [
        "**/*.lock",
        "**/package-lock.json",
        "**/dist/**",
        "**/*.min.js",
        "**/*.snap",
    ],
    "claude": {
        "bin": "claude",
        "model": None,
        "max_turns": 12,
        "timeout_s": 600,
        "allowed_tools": ["Read", "Grep", "Glob"],
        "disallowed_tools": [
            "Bash",
            "Edit",
            "Write",
            "NotebookEdit",
            "WebFetch",
            "WebSearch",
        ],
    },
}


def _merge(base: dict, override: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def load_config(repo: Path) -> dict:
    path = repo / AI_DIR / "config.json"
    if not path.exists():
        return copy.deepcopy(DEFAULTS)
    return _merge(DEFAULTS, json.loads(path.read_text()))
