"""Unit tests for the refresh_fixtures script's sanitize/assertion helpers."""
import importlib.util
import sys
from pathlib import Path

import pytest

# Load the script as a module (it's a top-level script, not a package).
SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "refresh_fixtures.py"
spec = importlib.util.spec_from_file_location("refresh_fixtures", SCRIPT_PATH)
refresh_fixtures = importlib.util.module_from_spec(spec)
sys.modules["refresh_fixtures"] = refresh_fixtures
spec.loader.exec_module(refresh_fixtures)


class TestSanitizeHtml:
    def test_replaces_github_owner_with_acme_org(self):
        html = '<a href="https://github.com/example-corp/some-repo/pull/1">'
        out = refresh_fixtures.sanitize_html(html)
        assert "example-corp" not in out
        assert "acme-org" in out
        # Repo name preserved.
        assert "some-repo" in out

    def test_replaces_user_login_meta(self):
        html = '<meta name="user-login" content="real-user-handle">'
        out = refresh_fixtures.sanitize_html(html)
        assert "real-user-handle" not in out
        assert "reviewer-bot" in out

    def test_replaces_avatar_url(self):
        html = '<img src="https://avatars.githubusercontent.com/u/12345?v=4">'
        out = refresh_fixtures.sanitize_html(html)
        assert "avatars.githubusercontent.com" not in out
        assert "avatars.example.com" in out

    def test_replaces_email(self):
        html = "<span>contact: someone@company-name.io</span>"
        out = refresh_fixtures.sanitize_html(html)
        assert "someone@company-name.io" not in out
        assert "placeholder@example.com" in out


class TestAssertNoKnownLeaks:
    def test_no_leaks_passes(self):
        refresh_fixtures.assert_no_known_leaks(
            '<a href="https://github.com/acme-org/some-repo">link</a>'
        )

    @pytest.mark.parametrize("leaky", [
        "Some-Company-That-Should-Not-Be-Here",
    ])
    def test_unknown_strings_dont_trigger(self, leaky):
        refresh_fixtures.assert_no_known_leaks(f"<p>{leaky}</p>")
