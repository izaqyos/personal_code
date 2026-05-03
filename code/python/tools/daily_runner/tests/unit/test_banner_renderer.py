"""Tests for the banner renderer (rich Panel composition + width adaptation)."""

from dataclasses import replace
from datetime import date

from src.banner.cadence import NextEvent
from src.banner.renderer import BannerData, render_banner_text, render_error_banner


def make_data(**overrides: object) -> BannerData:
    base = BannerData(
        today=date(2026, 4, 13),
        sprint_id="26.Q2.1",
        sprint_week=2,
        champion="yocheved",
        dod="yocheved",
        next_event=NextEvent("DR", date(2026, 4, 26), 13),
        free_text=None,
    )
    if not overrides:
        return base
    return replace(base, **overrides)


class TestRenderBannerText:
    def test_wide_layout_includes_all_default_fields(self) -> None:
        data = make_data()
        out = render_banner_text(data, width=100)

        assert "26.Q2.1" in out
        assert "Week 2" in out
        assert "Yocheved" in out  # title-cased
        assert "DR" in out
        assert "13d" in out

    def test_narrow_layout_uses_short_labels(self) -> None:
        data = make_data()
        out = render_banner_text(data, width=60)

        assert "26.Q2.1" in out
        assert "Champ" in out or "Champion" in out
        assert "DoD" in out

    def test_tiny_layout_no_panel_chrome(self) -> None:
        data = make_data()
        out = render_banner_text(data, width=35)

        # No box-drawing characters
        assert "╭" not in out
        assert "╰" not in out
        assert "26.Q2.1" in out

    def test_free_text_appears_when_provided(self) -> None:
        data = make_data(free_text="welcome back Muhe!")
        out = render_banner_text(data, width=100)

        assert "welcome back Muhe!" in out

    def test_free_text_only_no_cadence_fields(self) -> None:
        data = BannerData(
            today=date(2026, 4, 13),
            sprint_id=None,
            sprint_week=None,
            champion=None,
            dod=None,
            next_event=None,
            free_text="hello world",
        )
        out = render_banner_text(data, width=100)

        assert "hello world" in out
        assert "26.Q2" not in out

    def test_two_day_countdown_marked(self) -> None:
        data = make_data(next_event=NextEvent("DR", date(2026, 4, 15), 2))
        out = render_banner_text(data, width=100)
        assert "2d" in out

    def test_day_of_event_shown(self) -> None:
        data = make_data(next_event=NextEvent("DR", date(2026, 4, 13), 0))
        out = render_banner_text(data, width=100)
        assert "today" in out.lower() or "0d" in out


class TestRenderErrorBanner:
    def test_includes_path(self) -> None:
        out = render_error_banner(
            schedule_path="/tmp/schedules.json",
            reason="file not found",
            free_text=None,
            width=100,
        )

        assert "/tmp/schedules.json" in out
        assert "Banner unavailable" in out or "unavailable" in out.lower()

    def test_includes_fix_instructions(self) -> None:
        out = render_error_banner(
            schedule_path="/tmp/schedules.json",
            reason="file not found",
            free_text=None,
            width=100,
        )

        assert "schedules.example.json" in out
        assert "--no-banner" in out

    def test_appends_free_text_when_provided(self) -> None:
        out = render_error_banner(
            schedule_path="/tmp/x.json",
            reason="missing",
            free_text="welcome back",
            width=100,
        )
        assert "welcome back" in out

    def test_empty_reason_no_double_blank_line(self) -> None:
        """When reason is empty, the panel must not contain two consecutive blank body lines."""
        out = render_error_banner(
            schedule_path="/tmp/x.json",
            reason="",
            free_text=None,
            width=100,
        )
        # Strip rich panel chrome and check internal body lines.
        # Approximation: count consecutive blank lines (after stripping panel borders).
        # We check that the literal string "│\n│" or "│  \n│" patterns don't show
        # two whitespace-only lines back-to-back. Easier: check that the body has
        # only ONE blank-line gap between the path and the "Fix:" header.
        # Find the "Fix:" line index; the line just before it should be blank,
        # but two-before should not also be blank.
        lines = [ln.strip("│ \n\r") for ln in out.splitlines()]
        # Count blank lines between schedule_path and "Fix:"
        try:
            path_idx = next(i for i, ln in enumerate(lines) if "/tmp/x.json" in ln)
            fix_idx = next(i for i, ln in enumerate(lines) if ln == "Fix:")
        except StopIteration:
            raise AssertionError(f"missing markers in:\n{out}")
        between = lines[path_idx + 1:fix_idx]
        blanks = [ln for ln in between if ln == ""]
        assert len(blanks) == 1, f"expected exactly 1 blank line between path and Fix:, got {len(blanks)} in {between!r}"
