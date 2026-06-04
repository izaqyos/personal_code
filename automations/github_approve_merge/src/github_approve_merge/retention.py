from __future__ import annotations

import logging
import shutil
import time
from pathlib import Path

from github_approve_merge.config import RUN_ID_PATTERN

_log = logging.getLogger("gam")


def sweep(logs_root: Path, max_age_days: int, skip: set[Path]) -> list[Path]:
    """Delete run-dirs older than max_age_days. Return the list of paths actually deleted.

    Only deletes immediate children of logs_root that are directories AND whose
    name matches RUN_ID_PATTERN. This is structural: a stray file or
    differently-named dir cannot be deleted by accident.

    Never raises on individual delete failures — logs them at WARN and moves on.
    """
    if not logs_root.exists():
        return []

    threshold = time.time() - max_age_days * 86400
    deleted: list[Path] = []
    skip = {p.resolve() for p in skip}

    for child in logs_root.iterdir():
        if not child.is_dir():
            continue
        if not RUN_ID_PATTERN.match(child.name):
            continue
        if child.resolve() in skip:
            continue
        try:
            mtime = child.stat().st_mtime
        except OSError:
            continue
        if mtime >= threshold:
            continue

        try:
            shutil.rmtree(child, onerror=_rmtree_onerror)
        except OSError as e:
            _log.warning("retention: failed to delete %s: %s", child, e)
            continue
        deleted.append(child)

    return deleted


def _rmtree_onerror(func, path, exc_info):
    _log.warning("retention: rmtree could not remove %s (%s): %s", path, func.__name__, exc_info[1])
