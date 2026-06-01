from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from typing import Protocol


class GhError(RuntimeError):
    """Any non-zero `gh` invocation that isn't a more specific subclass."""


class GhAuthError(GhError):
    """gh not logged in, or token not SSO-authorized for the org."""


class GhNotFound(GhError):
    """PR or repo not found (404 / could-not-resolve)."""


@dataclass(frozen=True)
class RunResult:
    stdout: str
    stderr: str
    returncode: int


class Runner(Protocol):
    def __call__(self, argv: list[str]) -> RunResult: ...


def _subprocess_runner(argv: list[str]) -> RunResult:
    proc = subprocess.run(argv, capture_output=True, text=True)
    return RunResult(stdout=proc.stdout, stderr=proc.stderr, returncode=proc.returncode)


@dataclass
class FakeRunner:
    """Test runner. Records argv; returns canned result(s)."""

    stdout: str = ""
    stderr: str = ""
    returncode: int = 0
    calls: list[list[str]] = field(default_factory=list)
    # Optional queue of (stdout, stderr, rc) for multi-call sequences.
    queue: list[tuple[str, str, int]] = field(default_factory=list)

    def __call__(self, argv: list[str]) -> RunResult:
        self.calls.append(argv)
        if self.queue:
            out, err, rc = self.queue.pop(0)
            return RunResult(out, err, rc)
        return RunResult(self.stdout, self.stderr, self.returncode)


_AUTH_MARKERS = ("sso", "not logged", "authentication", "gh auth login", "bad credentials")
_NOTFOUND_MARKERS = ("could not resolve to a repository", "not found", "no pull requests found")


class GhClient:
    def __init__(self, runner: Runner | None = None):
        self._runner: Runner = runner or _subprocess_runner

    def _run(self, args: list[str]) -> str:
        argv = ["gh", *args]
        res = self._runner(argv)
        if res.returncode != 0:
            low = res.stderr.lower()
            if any(m in low for m in _AUTH_MARKERS):
                raise GhAuthError(res.stderr.strip() or "gh auth error")
            if any(m in low for m in _NOTFOUND_MARKERS):
                raise GhNotFound(res.stderr.strip() or "not found")
            raise GhError(res.stderr.strip() or f"gh exited {res.returncode}")
        return res.stdout
