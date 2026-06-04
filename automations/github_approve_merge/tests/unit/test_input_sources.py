import io
from pathlib import Path

import pytest

from github_approve_merge.input_sources import (
    InputSourceError,
    collect_urls,
    parse_url_file,
)
from github_approve_merge.url import PRRef


URL_A = "https://github.com/owner/repo/pull/1"
URL_B = "https://github.com/owner/repo/pull/2"
URL_C = "https://github.com/owner/repo/pull/3"

REF_A = PRRef("owner", "repo", 1)
REF_B = PRRef("owner", "repo", 2)
REF_C = PRRef("owner", "repo", 3)


class TestParseUrlFile:
    def test_one_per_line(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text(f"{URL_A}\n{URL_B}\n")
        assert parse_url_file(f) == [URL_A, URL_B]

    def test_strips_whitespace_blank_and_comments(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text(
            f"# header comment\n"
            f"\n"
            f"  {URL_A}  \n"
            f"# inline note\n"
            f"{URL_B}\n"
            f"\n"
        )
        assert parse_url_file(f) == [URL_A, URL_B]

    def test_missing_file_raises_input_source_error(self, tmp_path: Path):
        with pytest.raises(InputSourceError):
            parse_url_file(tmp_path / "nope.txt")


class TestCollectUrls:
    def test_args_only(self):
        refs = collect_urls(args=[URL_A, URL_B], file_path=None, stdin=None)
        assert refs == [REF_A, REF_B]

    def test_args_plus_file(self, tmp_path: Path):
        f = tmp_path / "urls.txt"
        f.write_text(f"{URL_B}\n{URL_C}\n")
        refs = collect_urls(args=[URL_A], file_path=f, stdin=None)
        assert refs == [REF_A, REF_B, REF_C]

    def test_stdin_only(self):
        refs = collect_urls(args=[], file_path=None, stdin=io.StringIO(f"{URL_A}\n{URL_B}\n"))
        assert refs == [REF_A, REF_B]

    def test_dedupe_first_occurrence_wins(self):
        refs = collect_urls(
            args=[URL_A, URL_B, URL_A],
            file_path=None,
            stdin=io.StringIO(f"{URL_B}\n{URL_C}\n"),
        )
        assert refs == [REF_A, REF_B, REF_C]

    def test_empty_inputs_raises(self):
        with pytest.raises(InputSourceError, match="no URLs"):
            collect_urls(args=[], file_path=None, stdin=None)

    def test_invalid_url_raises_with_source_context(self):
        with pytest.raises(InputSourceError, match=r"args\[1\]"):
            collect_urls(args=[URL_A, "not a url"], file_path=None, stdin=None)
