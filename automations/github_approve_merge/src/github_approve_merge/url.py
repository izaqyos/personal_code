from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

_PR_PATH_RE = re.compile(r"^/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<number>\d+)(?:/(?:files|commits))?/?$")


@dataclass(frozen=True, slots=True)
class PRRef:
    owner: str
    repo: str
    number: int

    def __str__(self) -> str:
        return f"{self.owner}/{self.repo}#{self.number}"


def parse_pr_url(url: str) -> PRRef:
    """Parse a github.com PR URL into a PRRef.

    Accepts canonical forms and the /files, /commits suffixes, plus trailing
    slashes, query strings, and fragments. Rejects non-github.com hosts (V1
    is github.com only) and anything that doesn't match the PR path shape.
    """
    if not url or not isinstance(url, str):
        raise ValueError(f"empty or non-string url: {url!r}")

    parsed = urlparse(url.strip())
    if parsed.scheme != "https":
        raise ValueError(f"only https URLs are accepted (got scheme={parsed.scheme!r}): {url!r}")
    if parsed.netloc != "github.com":
        raise ValueError(
            f"only github.com is supported in V1 (got host={parsed.netloc!r}): {url!r}"
        )

    m = _PR_PATH_RE.match(parsed.path)
    if not m:
        raise ValueError(f"not a recognizable PR URL path: {url!r}")

    return PRRef(owner=m["owner"], repo=m["repo"], number=int(m["number"]))
