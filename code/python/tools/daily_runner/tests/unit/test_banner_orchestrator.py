"""Integration tests for the banner orchestrator."""

import json
from datetime import date
from pathlib import Path
from types import SimpleNamespace

import pytest

from src.banner import render_banner
from src.core.models import BannerConfig

VALID_DATA = {
    "team_members": {"yocheved": "U1"},
    "rotation_schedule": {
        "26.Q2.1": {
            "champion": "yocheved",
            "dr": "2026-04-26",
            "go_nogo": "2026-04-30",
            "prod": "2026-05-03",
        },
    },
    "dod_schedule": {"2026-04-12": "chen"},
}


def make_args(**kwargs: object) -> SimpleNamespace:
    defaults: dict[str, object] = {
        "banner_value": None,
        "banner_fields": None,
        "banner_text": None,
        "no_banner": False,
    }
    defaults.update(kwargs)
    return SimpleNamespace(**defaults)


@pytest.fixture
def schedules_file(tmp_path: Path) -> Path:
    p = tmp_path / "schedules.json"
    p.write_text(json.dumps(VALID_DATA))
    return p


class TestRenderBanner:
    def test_returns_none_when_banner_disabled(self) -> None:
        cfg = BannerConfig(enabled=False)
        result = render_banner(make_args(), cfg, today=date(2026, 4, 13), width=100)
        assert result is None

    def test_returns_none_when_no_banner_overrides(self) -> None:
        cfg = BannerConfig(enabled=True)
        args = make_args(no_banner=True)
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)
        assert result is None

    def test_free_text_only_skips_loader(self) -> None:
        cfg = BannerConfig(enabled=False, schedules_path="/nonexistent/path.json")
        args = make_args(banner_value="", banner_text="hello world")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "hello world" in result
        # No error banner because loader was never called
        assert "unavailable" not in result.lower()

    def test_full_banner_renders_cadence(self, schedules_file: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(schedules_file),
            default_fields=["sprint", "champion"],
        )
        args = make_args(banner_value="")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "26.Q2.1" in result
        assert "Yocheved" in result

    def test_explicit_fields_override_defaults(self, schedules_file: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(schedules_file),
            default_fields=["sprint", "champion"],
        )
        args = make_args(banner_value="", banner_fields=["dod"])
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        # dod for 2026-04-12 (Sunday) is "chen"
        assert "Chen" in result

    def test_missing_schedule_file_renders_error_banner(self, tmp_path: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(tmp_path / "nope.json"),
        )
        args = make_args(banner_value="")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "unavailable" in result.lower()
        assert "nope.json" in result
        # Path should appear exactly once — no redundant reason line restating the headline.
        assert result.count("nope.json") == 1

    def test_missing_schedule_with_text_appends_text(self, tmp_path: Path) -> None:
        cfg = BannerConfig(
            enabled=True,
            schedules_path=str(tmp_path / "nope.json"),
        )
        args = make_args(banner_value="", banner_text="welcome back")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "welcome back" in result

    def test_explicit_fields_with_text_loads_schedules(self, schedules_file: Path) -> None:
        """`-b sprint --banner-text 'hi'` with cfg.enabled=False must still load cadence."""
        cfg = BannerConfig(
            enabled=False,
            schedules_path=str(schedules_file),
            default_fields=["sprint"],
        )
        args = make_args(banner_value="sprint", banner_fields=["sprint"], banner_text="hi")
        result = render_banner(args, cfg, today=date(2026, 4, 13), width=100)

        assert result is not None
        assert "26.Q2.1" in result  # sprint loaded from schedules
        assert "hi" in result        # text appears too
