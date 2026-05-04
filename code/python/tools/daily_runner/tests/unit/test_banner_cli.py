"""Tests for banner CLI flag parsing and disambiguation."""

from pathlib import Path

import pytest

from main import KNOWN_BANNER_FIELDS, _build_parser, _parse_banner_value


class TestParseBannerValue:
    @pytest.mark.parametrize(
        "value, known, expected",
        [
            (None, {"sprint", "dod"}, (None, None)),
            ("", {"sprint", "dod"}, (None, None)),
            ("sprint,dod", {"sprint", "dod"}, (["sprint", "dod"], None)),
            ("sprint", {"sprint", "dod"}, (["sprint"], None)),
            ("welcome back Muhe", {"sprint", "dod"}, (None, "welcome back Muhe")),
            ("hello", {"sprint", "dod"}, (None, "hello")),
            ("sprint,unknown", {"sprint", "dod"}, (None, "sprint,unknown")),
            ("Sprint", {"sprint", "dod"}, (None, "Sprint")),
        ],
    )
    def test_disambiguates(
        self,
        value: str | None,
        known: set[str],
        expected: tuple[list[str] | None, str | None],
    ) -> None:
        assert _parse_banner_value(value, known) == expected


class TestBannerArgs:
    def test_no_banner_flags_default(self) -> None:
        parser = _build_parser()
        args = parser.parse_args([])

        assert args.banner_value is None
        assert args.banner_fields is None
        assert args.banner_text is None
        assert args.no_banner is False

    def test_bare_b_flag(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["-b"])
        assert args.banner_value == ""

    def test_b_with_fields(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["-b", "sprint,dod"])
        assert args.banner_value == "sprint,dod"

    def test_b_with_free_text(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["-b", "welcome back Muhe"])
        assert args.banner_value == "welcome back Muhe"

    def test_explicit_fields_and_text(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(
            ["--banner-fields", "sprint,dod", "--banner-text", "hi"]
        )
        assert args.banner_fields == ["sprint", "dod"]
        assert args.banner_text == "hi"

    def test_no_banner(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["--no-banner"])
        assert args.no_banner is True

    def test_banner_text_only_enables_banner(self) -> None:
        """Without -b, but with --banner-text, banner should still be on."""
        from src.banner import _resolve_intent
        parser = _build_parser()
        args = parser.parse_args(["--banner-text", "hi"])
        on, _fields, text = _resolve_intent(args, config_enabled=False)
        assert on is True
        assert text == "hi"


class TestBannerInCliMode:
    """Smoke test: -b causes banner output on stdout before cli_main runs."""

    def test_banner_printed_before_cli(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        import json
        from unittest.mock import patch

        # Create example schedule
        sched_path = tmp_path / "schedules.json"
        sched_path.write_text(
            json.dumps(
                {
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
            )
        )

        # Create a minimal config.json pointing at it
        cfg_path = tmp_path / "config.json"
        cfg_path.write_text(
            json.dumps(
                {
                    "version": "1.0",
                    "banner": {
                        "enabled": False,
                        "schedules_path": str(sched_path),
                        "default_fields": ["sprint", "champion"],
                    },
                }
            )
        )

        # Mock cli_main to a no-op returning 0
        with patch("src.cli.app.main", return_value=0):
            monkeypatch.chdir(tmp_path)
            monkeypatch.setattr(
                "sys.argv",
                ["daily-timer", "--mode", "cli", "--config", str(cfg_path), "-b"],
            )
            from main import main as run

            rc = run()

        captured = capsys.readouterr()
        assert rc == 0
        assert "26.Q2.1" in captured.out or "Yocheved" in captured.out
