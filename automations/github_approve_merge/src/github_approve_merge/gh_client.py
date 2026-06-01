from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field, replace
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

# NB: `locked` is NOT a valid `gh pr view --json` field (not in gh's allowlist), so we
# fetch it separately from the REST pulls endpoint in fetch_pr().
_PR_FIELDS = "number,state,isDraft,mergeable,mergeStateStatus,reviewDecision,author,baseRefName,reviews"

_METHOD_FLAG = {"merge": "--merge", "squash": "--squash", "rebase": "--rebase"}
# Repo allow-flag key per method, checked in this order for fallback.
_METHOD_ALLOW_KEY = {
    "merge": "allow_merge_commit",
    "squash": "allow_squash_merge",
    "rebase": "allow_rebase_merge",
}
_log = logging.getLogger("gam")


@dataclass(frozen=True)
class GhPR:
    number: int
    state: str               # OPEN | CLOSED | MERGED
    is_draft: bool
    locked: bool
    mergeable: str           # MERGEABLE | CONFLICTING | UNKNOWN
    merge_state_status: str  # CLEAN | BLOCKED | BEHIND | DIRTY | UNSTABLE | HAS_HOOKS | DRAFT | UNKNOWN
    review_decision: str     # APPROVED | REVIEW_REQUIRED | CHANGES_REQUESTED | ""
    author_login: str
    base_ref: str
    reviews: list[dict]

    def approved_by(self, login: str) -> bool:
        """True iff the latest review by `login` is APPROVED."""
        latest = None
        for r in self.reviews:
            if (r.get("author") or {}).get("login") == login:
                latest = r.get("state")
        return latest == "APPROVED"

    @classmethod
    def from_json(cls, raw: str) -> "GhPR":
        d = json.loads(raw)
        return cls(
            number=d["number"],
            state=d.get("state", ""),
            is_draft=bool(d.get("isDraft", False)),
            locked=bool(d.get("locked", False)),
            mergeable=d.get("mergeable", "UNKNOWN"),
            merge_state_status=d.get("mergeStateStatus", "UNKNOWN"),
            review_decision=d.get("reviewDecision") or "",
            author_login=(d.get("author") or {}).get("login", ""),
            base_ref=d.get("baseRefName", ""),
            reviews=d.get("reviews", []),
        )


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

    # --- reads ------------------------------------------------------------

    def preflight(self) -> None:
        """Raise GhAuthError if gh is missing or not logged in. `gh auth status`
        exits non-zero when logged out."""
        self._run(["auth", "status"])

    def current_login(self) -> str:
        return self._run(["api", "user", "--jq", ".login"]).strip()

    def fetch_pr(self, owner: str, repo: str, number: int) -> GhPR:
        out = self._run([
            "pr", "view", str(number), "--repo", f"{owner}/{repo}",
            "--json", _PR_FIELDS,
        ])
        pr = GhPR.from_json(out)
        # `locked` isn't available via `gh pr view --json`; read it from REST.
        locked = self._run([
            "api", f"repos/{owner}/{repo}/pulls/{number}", "--jq", ".locked",
        ]).strip()
        return replace(pr, locked=(locked == "true"))

    def has_merge_queue(self, owner: str, repo: str, branch: str) -> bool:
        q = ("query($o:String!,$r:String!,$b:String!){repository(owner:$o,name:$r)"
             "{mergeQueue(branch:$b){id}}}")
        out = self._run([
            "api", "graphql", "-f", f"query={q}",
            "-F", f"o={owner}", "-F", f"r={repo}", "-F", f"b={branch}",
        ])
        node = (((json.loads(out).get("data") or {}).get("repository") or {})
                .get("mergeQueue"))
        return node is not None

    # --- writes -----------------------------------------------------------

    def approve(self, owner: str, repo: str, number: int) -> None:
        self._run(["pr", "review", str(number), "--repo", f"{owner}/{repo}", "--approve"])

    def _node_id(self, owner: str, repo: str, number: int) -> str:
        q = ("query($o:String!,$r:String!,$n:Int!){repository(owner:$o,name:$r)"
             "{pullRequest(number:$n){id}}}")
        out = self._run([
            "api", "graphql", "-f", f"query={q}",
            "-F", f"o={owner}", "-F", f"r={repo}", "-F", f"n={number}",
        ])
        return json.loads(out)["data"]["repository"]["pullRequest"]["id"]

    def enqueue(self, owner: str, repo: str, number: int) -> None:
        pr_id = self._node_id(owner, repo, number)
        m = ("mutation($id:ID!){enqueuePullRequest(input:{pullRequestId:$id})"
             "{mergeQueueEntry{state}}}")
        self._run(["api", "graphql", "-f", f"query={m}", "-F", f"id={pr_id}"])

    def direct_merge(self, owner: str, repo: str, number: int, *, method: str) -> None:
        try:
            self._run(["pr", "merge", str(number), "--repo", f"{owner}/{repo}",
                       _METHOD_FLAG[method]])
        except GhError as e:
            if "not allowed" not in str(e).lower():
                raise
            fallback = self._first_allowed_method(owner, repo)
            _log.warning("merge method %r disallowed on %s/%s; falling back to %r",
                         method, owner, repo, fallback)
            self._run(["pr", "merge", str(number), "--repo", f"{owner}/{repo}",
                       _METHOD_FLAG[fallback]])

    def _first_allowed_method(self, owner: str, repo: str) -> str:
        out = self._run([
            "api", f"repos/{owner}/{repo}", "--jq",
            "{allow_merge_commit:.allow_merge_commit,"
            "allow_squash_merge:.allow_squash_merge,"
            "allow_rebase_merge:.allow_rebase_merge}",
        ])
        flags = json.loads(out)
        for method in ("merge", "squash", "rebase"):
            if flags.get(_METHOD_ALLOW_KEY[method]):
                return method
        raise GhError(f"no merge method allowed on {owner}/{repo}")

    def enable_auto_merge(self, owner: str, repo: str, number: int, *, method: str) -> None:
        self._run(["pr", "merge", str(number), "--repo", f"{owner}/{repo}",
                   "--auto", _METHOD_FLAG[method]])


@dataclass
class PrClient:
    """Binds a GhClient + PR coordinates so process_pr stays PR-centric. Caches the
    merge-queue probe across the per-PR flow (classify may be called twice)."""

    gh: GhClient
    owner: str
    repo: str
    number: int
    me: str
    _has_queue: bool | None = None

    def classify(self, _pr):
        from github_approve_merge.pr_state import classify as _classify
        pr = self.gh.fetch_pr(self.owner, self.repo, self.number)
        if self._has_queue is None:
            self._has_queue = self.gh.has_merge_queue(self.owner, self.repo, pr.base_ref)
        return _classify(pr, me=self.me, has_queue=self._has_queue)

    def has_queue(self, _pr):
        return bool(self._has_queue)

    def approve(self, _pr):
        self.gh.approve(self.owner, self.repo, self.number)

    def enqueue(self, _pr):
        self.gh.enqueue(self.owner, self.repo, self.number)

    def direct_merge(self, _pr, method):
        self.gh.direct_merge(self.owner, self.repo, self.number, method=method)

    def enable_auto_merge(self, _pr, method):
        self.gh.enable_auto_merge(self.owner, self.repo, self.number, method=method)
