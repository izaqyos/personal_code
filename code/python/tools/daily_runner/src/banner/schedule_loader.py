"""Loads and validates schedules.json from disk."""

import json
from pathlib import Path

from pydantic import ValidationError

from src.banner.errors import MalformedScheduleError, MissingScheduleError
from src.banner.models import Schedules


def load_schedules(path: Path) -> Schedules:
    """Load schedules.json from path. Raises BannerError subclasses on failure.

    Args:
        path: Path to schedules.json. Empty paths and `~`-prefixed paths are
            handled. Tilde is expanded against $HOME.

    Returns:
        A validated `Schedules` instance.

    Raises:
        MissingScheduleError: file is missing or path is empty.
        MalformedScheduleError: file is unreadable JSON or fails validation.
    """
    if not str(path):
        raise MissingScheduleError("")

    resolved = Path(str(path)).expanduser()

    if not resolved.is_file():
        raise MissingScheduleError(str(resolved))

    try:
        raw = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MalformedScheduleError(f"invalid JSON: {exc}") from exc

    try:
        return Schedules.model_validate(raw)
    except ValidationError as exc:
        raise MalformedScheduleError(str(exc)) from exc
