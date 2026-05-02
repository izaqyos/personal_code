"""Tests for banner error types."""

import pytest

from src.banner.errors import BannerError, MalformedScheduleError, MissingScheduleError


class TestBannerErrors:
    def test_banner_error_is_base_exception(self) -> None:
        assert issubclass(BannerError, Exception)

    def test_missing_schedule_error_is_banner_error(self) -> None:
        assert issubclass(MissingScheduleError, BannerError)

    def test_malformed_schedule_error_is_banner_error(self) -> None:
        assert issubclass(MalformedScheduleError, BannerError)

    def test_missing_schedule_carries_path(self) -> None:
        err = MissingScheduleError("/some/path/schedules.json")
        assert err.path == "/some/path/schedules.json"
        assert "/some/path/schedules.json" in str(err)

    def test_malformed_schedule_carries_reason(self) -> None:
        err = MalformedScheduleError("missing key: rotation_schedule")
        assert err.reason == "missing key: rotation_schedule"
        assert "missing key: rotation_schedule" in str(err)
