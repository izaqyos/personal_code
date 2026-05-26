import pytest

from github_approve_merge.url import PRRef, parse_pr_url


class TestParsePrUrl:
    def test_canonical_url(self):
        assert parse_pr_url("https://github.com/acme-org/widgets-service/pull/561") == PRRef(
            owner="acme-org", repo="widgets-service", number=561
        )

    def test_trailing_slash(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1/") == PRRef("owner", "repo", 1)

    def test_files_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1/files") == PRRef("owner", "repo", 1)

    def test_commits_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1/commits") == PRRef("owner", "repo", 1)

    def test_fragment_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1#discussion_r123") == PRRef("owner", "repo", 1)

    def test_query_suffix(self):
        assert parse_pr_url("https://github.com/owner/repo/pull/1?diff=split") == PRRef("owner", "repo", 1)

    @pytest.mark.parametrize("bad_url", [
        "",
        "not a url",
        "ftp://github.com/owner/repo/pull/1",
        "http://github.com/owner/repo/pull/1",                   # http not https
        "https://example.com/owner/repo/pull/1",                 # wrong host
        "https://ghe.internal.example/owner/repo/pull/1",        # GHES, out of V1 scope
        "https://github.com/owner/repo/issues/1",                # not a PR
        "https://github.com/owner/repo/pull/abc",                # non-numeric
        "https://github.com/owner/repo/pull/",                   # no number
        "https://github.com/owner/repo/pulls/1",                 # plural
        "https://github.com/owner/repo",                         # not a PR url
    ])
    def test_bad_url_raises_value_error(self, bad_url):
        with pytest.raises(ValueError):
            parse_pr_url(bad_url)


class TestPrRefStr:
    def test_str_format(self):
        assert str(PRRef("acme-org", "widgets-service", 561)) == \
            "acme-org/widgets-service#561"
