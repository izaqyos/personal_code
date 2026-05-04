"""Tests for banner CLI flag parsing and disambiguation."""

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
