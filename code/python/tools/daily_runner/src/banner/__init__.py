"""Banner module for daily_runner CLI: cadence info + free text before standup."""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Protocol

from src.banner.cadence import current_sprint, dod_for, next_event, sprint_week
from src.banner.errors import BannerError, MalformedScheduleError, MissingScheduleError
from src.banner.renderer import BannerData, render_banner_text, render_error_banner
from src.banner.schedule_loader import load_schedules


class _Args(Protocol):
    banner_value: str | None
    banner_fields: list[str] | None
    banner_text: str | None
    no_banner: bool


def _resolve_intent(args: _Args, config_enabled: bool) -> tuple[bool, list[str] | None, str | None]:
    """Return (banner_on, fields_or_None_for_default, free_text_or_None).

    Banner is ON if any banner-* CLI flag was passed OR config.enabled is True.
    --no-banner overrides everything.
    """
    if getattr(args, "no_banner", False):
        return (False, None, None)

    fields = getattr(args, "banner_fields", None)
    text = getattr(args, "banner_text", None)
    bare_b = getattr(args, "banner_value", None) is not None
    any_flag = bare_b or fields is not None or text is not None
    on = any_flag or config_enabled

    return (on, fields, text)


def render_banner(
    args: _Args,
    config: Any,
    today: date | None = None,
    width: int | None = None,
) -> str | None:
    """Top-level entrypoint. Returns rendered banner string or None if banner is off.

    Args:
        args: argparse Namespace with banner flags.
        config: BannerConfig instance (enabled, schedules_path, default_fields).
        today: Date used for cadence math; defaults to date.today().
        width: Terminal width override; defaults to rich's autodetected width.
    """
    on, override_fields, free_text = _resolve_intent(args, getattr(config, "enabled", False))
    if not on:
        return None

    if today is None:
        today = date.today()

    if width is None:
        from rich.console import Console
        width = Console().width

    fields = override_fields if override_fields is not None else list(config.default_fields)

    # Free-text-only: skip the loader when the user supplied free text AND
    # did not explicitly opt into cadence — neither via --banner-fields nor
    # via config.enabled. This covers `--banner-text "hi"` alone, or `-b
    # --banner-text "hi"` with config disabled. If override_fields is set
    # (even to []), the user made an explicit choice and we honor it; if
    # config.enabled is True, the user opted in via config and we honor that too.
    text_only = (
        free_text is not None
        and override_fields is None
        and not getattr(config, "enabled", False)
    )
    if text_only:
        data = BannerData(
            today=today,
            sprint_id=None,
            sprint_week=None,
            champion=None,
            dod=None,
            next_event=None,
            free_text=free_text,
        )
        return render_banner_text(data, width)

    if not fields:
        return None

    # Load schedules.
    schedules_path = getattr(config, "schedules_path", "") or ""
    try:
        sched = load_schedules(Path(schedules_path)) if schedules_path else None
        if sched is None:
            raise MissingScheduleError("")
    except BannerError as exc:
        reason = exc.reason if isinstance(exc, MalformedScheduleError) else str(exc)
        return render_error_banner(
            schedule_path=schedules_path or "(not configured)",
            reason=reason,
            free_text=free_text,
            width=width,
        )

    sprint_id = current_sprint(sched, today) if "sprint" in fields or "sprint_week" in fields else None
    week = sprint_week(sched, sprint_id, today) if sprint_id and "sprint_week" in fields else None
    champion = sched.rotation_schedule[sprint_id].champion if sprint_id and "champion" in fields else None
    dod = dod_for(sched, today) if "dod" in fields else None
    ev = next_event(sched, today) if "next_event" in fields else None

    data = BannerData(
        today=today,
        sprint_id=sprint_id if "sprint" in fields else None,
        sprint_week=week,
        champion=champion,
        dod=dod,
        next_event=ev,
        free_text=free_text,
    )
    return render_banner_text(data, width)


__all__ = ["render_banner", "_resolve_intent"]
