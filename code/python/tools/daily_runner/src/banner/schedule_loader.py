"""Loads and validates schedules.json from disk."""

import json
from pathlib import Path

from pydantic import ValidationError

from src.banner.errors import MalformedScheduleError, MissingScheduleError
from src.banner.models import Schedules


def _format_validation_error(exc: ValidationError) -> str:
    """Format a pydantic ValidationError as a one-line summary.

    Returns the first error's location and message, plus a count if there are more.
    """
    errors = exc.errors()
    if not errors:
        return "validation failed"
    first = errors[0]
    loc = ".".join(str(p) for p in first.get("loc", ()))
    msg = first.get("msg", "validation failed")
    summary = f"{loc}: {msg}" if loc else msg
    if len(errors) > 1:
        summary += f" (and {len(errors) - 1} more)"
    return summary


def load_schedules(path: Path) -> Schedules:
    """Load schedules.json from path. Raises BannerError subclasses on failure.

    Args:
        path: Path to schedules.json. Empty paths are rejected (they resolve
            to the current directory). `~`-prefixed paths are expanded against
            $HOME.

    Returns:
        A validated `Schedules` instance.

    Raises:
        MissingScheduleError: file is missing or path doesn't point at a file.
        MalformedScheduleError: file is unreadable JSON or fails validation.
    """
    resolved = path.expanduser()

    if not resolved.is_file():
        raise MissingScheduleError(str(resolved))

    try:
        raw = json.loads(resolved.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise MalformedScheduleError(f"invalid JSON: {exc}") from exc

    try:
        return Schedules.model_validate(raw)
    except ValidationError as exc:
        raise MalformedScheduleError(_format_validation_error(exc)) from exc
