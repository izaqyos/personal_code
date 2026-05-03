"""Renders banner data as a rich Panel string. Handles width adaptation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from io import StringIO

from rich.console import Console
from rich.panel import Panel

from src.banner.cadence import NextEvent

WIDE_THRESHOLD = 80
TINY_THRESHOLD = 40


@dataclass
class BannerData:
    today: date
    sprint_id: str | None
    sprint_week: int | None
    champion: str | None
    dod: str | None
    next_event: NextEvent | None
    free_text: str | None


def _name(value: str | None) -> str:
    if not value:
        return "?"
    return value[:1].upper() + value[1:]


def _short_name(value: str | None) -> str:
    if not value:
        return "?"
    return _name(value)[:4]


def _countdown_str(ev: NextEvent) -> str:
    if ev.days_until == 0:
        return f"{ev.label} today · {ev.target.strftime('%a %b %d')}"
    return f"{ev.label} in {ev.days_until}d · {ev.target.strftime('%a %b %d')}"


def _short_countdown_str(ev: NextEvent) -> str:
    if ev.days_until == 0:
        return f"{ev.label} today"
    return f"{ev.label} in {ev.days_until}d"


def _capture(renderable: object, width: int) -> str:
    buf = StringIO()
    console = Console(file=buf, width=width, force_terminal=False, no_color=True)
    console.print(renderable)
    return buf.getvalue()


def _render_wide(data: BannerData, width: int) -> str:
    title_parts = []
    if data.sprint_id:
        title_parts.append(f"Sprint {data.sprint_id}")
    if data.sprint_week:
        title_parts.append(f"Week {data.sprint_week}")
    title_parts.append(data.today.strftime("%a %b %d"))
    title = " · ".join(title_parts)

    lines: list[str] = []
    if data.champion or data.dod:
        body = []
        if data.champion:
            body.append(f"Champion: {_name(data.champion)}")
        if data.dod:
            body.append(f"DoD: {_name(data.dod)}")
        lines.append("  ".join(body))
    if data.next_event:
        lines.append(_countdown_str(data.next_event))
    if data.free_text:
        lines.append(data.free_text)

    body = "\n".join(lines) if lines else " "
    panel = Panel(body, title=title, border_style="cyan", width=width)
    return _capture(panel, width)


def _render_narrow(data: BannerData, width: int) -> str:
    title_parts = []
    if data.sprint_id:
        title_parts.append(data.sprint_id)
    if data.sprint_week:
        title_parts.append(f"W{data.sprint_week}")
    title_parts.append(data.today.strftime("%b %d"))
    title = " · ".join(title_parts)

    lines: list[str] = []
    if data.champion or data.dod:
        parts = []
        if data.champion:
            parts.append(f"Champ: {_short_name(data.champion)}")
        if data.dod:
            parts.append(f"DoD: {_short_name(data.dod)}")
        lines.append("   ".join(parts))
    if data.next_event:
        lines.append(_short_countdown_str(data.next_event))
    if data.free_text:
        lines.append(data.free_text)

    body = "\n".join(lines) if lines else " "
    panel = Panel(body, title=title, border_style="cyan", width=width)
    return _capture(panel, width)


def _render_tiny(data: BannerData, width: int) -> str:
    parts: list[str] = []
    if data.sprint_id:
        sp = data.sprint_id
        if data.sprint_week:
            sp += f" W{data.sprint_week}"
        parts.append(sp)
    if data.champion:
        parts.append(f"Champ:{_short_name(data.champion)}")
    if data.dod:
        parts.append(f"DoD:{_short_name(data.dod)}")
    if data.next_event:
        parts.append(_short_countdown_str(data.next_event))
    line = " | ".join(parts)
    if data.free_text:
        return f"{line}\n{data.free_text}\n" if line else f"{data.free_text}\n"
    return line + "\n"


def render_banner_text(data: BannerData, width: int) -> str:
    if width < TINY_THRESHOLD:
        return _render_tiny(data, width)
    if width < WIDE_THRESHOLD:
        return _render_narrow(data, width)
    return _render_wide(data, width)


def render_error_banner(
    schedule_path: str,
    reason: str,
    free_text: str | None,
    width: int,
) -> str:
    body_lines = [
        "schedules.json not found at:",
        f"  {schedule_path}",
        f"  ({reason})" if reason else "",
        "",
        "Fix:",
        "  1. Set banner.schedules_path in config.json",
        "  2. Or copy the example:",
        "     cp config/schedules.example.json \\",
        "        config/schedules.json",
        "  3. Or run with --no-banner to suppress",
    ]
    body = "\n".join(line for line in body_lines if line is not None)
    panel = Panel(
        body,
        title="⚠ Banner unavailable",
        border_style="yellow",
        width=max(width, TINY_THRESHOLD),
    )
    out = _capture(panel, max(width, TINY_THRESHOLD))
    if free_text:
        out += f"{free_text}\n"
    return out
