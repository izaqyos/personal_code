# github_approve_merge v2 (API Backend) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Playwright/storage_state backend with the GitHub API via the `gh` CLI, add an explicit human merge gate, and keep batch/observability/resume.

**Architecture:** A single seam (`gh_client.py`) wraps every `gh` subprocess call and maps failures to typed errors. `pr_state.py` classifies from structured `gh pr view --json` fields (no DOM). `actions.py` drives per-PR approve→merge with auto-detected merge action (queue-enqueue / direct-merge / auto-merge) behind a confirmation gate. `runner.py`/`retention.py`/`logging_setup.py`/`input_sources.py`/`url.py` are kept; the browser stack is deleted.

**Tech Stack:** Python 3.12, `uv`, `gh` CLI (subprocess), `pytest` + `pytest-asyncio` (async kept for minimal churn; `gh_client` calls are sync via `asyncio.to_thread`), stdlib `logging`, `subprocess`, `json`.

**Reference spec:** `docs/superpowers/specs/2026-06-01-github-approve-merge-api-backend-design.md`

---

## File Structure

```
src/github_approve_merge/
  gh_client.py     CREATE  subprocess seam + typed errors + GhPR dataclass
  pr_state.py      REWRITE classify(GhPR, me, has_queue) -> (PRState, flags)
  merge_action.py  CREATE  pure selector: (state, has_queue) -> MergeAction enum
  actions.py       MODIFY  process_pr uses gh_client + merge_action; new statuses
  gate.py          CREATE  plan table + confirmation logic
  cli.py           MODIFY  verbs: auth status/doctor, approve, merge, run, gc
  runner.py        MODIFY  pass approve/do_merge/method/gate flags through; gate hook
  config.py        MODIFY  drop storage_state/headless; keep logs_dir/retention
  retention.py     KEEP
  logging_setup.py KEEP
  input_sources.py KEEP
  url.py           KEEP

DELETE: browser.py, auth.py, screenshots.py, pages/ (whole dir),
        tests/pages/ (whole dir), tests/fixtures/html/ (whole dir),
        scripts/refresh_fixtures.py, tests/live/test_smoke.py (replace).

tests/
  unit/test_gh_client.py     CREATE
  unit/test_pr_state_api.py  CREATE (replaces tests/pages/test_detect_state.py)
  unit/test_merge_action.py  CREATE
  unit/test_gate.py          CREATE
  unit/test_process_pr.py    REWRITE against fakes (no page objects)
  unit/test_cli.py           MODIFY (verbs)
  live/test_smoke.py         REWRITE (gh read-only)
  fixtures/json/*.json       CREATE sanitized gh pr view captures
```

---

## Phase 0 — Branch & teardown

### Task 0: Create branch and delete the browser stack

**Files:**
- Delete: `src/github_approve_merge/browser.py`, `auth.py`, `screenshots.py`, `pages/` (dir)
- Delete: `tests/pages/` (dir), `tests/fixtures/html/` (dir), `scripts/refresh_fixtures.py`
- Modify: `pyproject.toml` (drop `playwright` dep)

- [ ] **Step 1: Branch from main**

```bash
cd /Users/yosii/work/git/personal_code/automations/github_approve_merge
git checkout main
git checkout -b feat/api-backend-v2
```

- [ ] **Step 2: Delete browser modules and their tests**

```bash
git rm -r src/github_approve_merge/pages tests/pages tests/fixtures/html \
        src/github_approve_merge/browser.py \
        src/github_approve_merge/auth.py \
        src/github_approve_merge/screenshots.py \
        scripts/refresh_fixtures.py
```

- [ ] **Step 3: Drop the Playwright dependency**

Edit `pyproject.toml`: remove the `playwright` line from `dependencies`. Leave `pytest`, `pytest-asyncio`.

- [ ] **Step 4: Sync env**

Run: `uv sync`
Expected: resolves without playwright; no error.

- [ ] **Step 5: Commit**

```bash
git add -A
git commit -m "chore(github_approve_merge): remove Playwright browser stack for API backend"
```

> Note: the suite will not pass until Phase 1–4 land — that's expected for this teardown commit. Do not run the full suite here.

---

## Phase 1 — gh_client seam

### Task 1: `GhError` hierarchy + `_run` runner

**Files:**
- Create: `src/github_approve_merge/gh_client.py`
- Test: `tests/unit/test_gh_client.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_gh_client.py
import pytest
from github_approve_merge import gh_client as gc


def test_run_returns_stdout_on_success():
    fake = gc.FakeRunner(stdout='{"ok": true}', stderr="", returncode=0)
    client = gc.GhClient(runner=fake)
    assert client._run(["api", "user"]) == '{"ok": true}'
    assert fake.calls == [["gh", "api", "user"]]


def test_run_raises_auth_error_on_sso_message():
    fake = gc.FakeRunner(stdout="", stderr="SSO authorization required", returncode=1)
    client = gc.GhClient(runner=fake)
    with pytest.raises(gc.GhAuthError):
        client._run(["pr", "view", "1"])


def test_run_raises_not_found_on_404():
    fake = gc.FakeRunner(stdout="", stderr="Could not resolve to a Repository", returncode=1)
    client = gc.GhClient(runner=fake)
    with pytest.raises(gc.GhNotFound):
        client._run(["pr", "view", "1"])


def test_run_raises_generic_on_other_failure():
    fake = gc.FakeRunner(stdout="", stderr="boom", returncode=1)
    client = gc.GhClient(runner=fake)
    with pytest.raises(gc.GhError):
        client._run(["pr", "view", "1"])
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_gh_client.py -q`
Expected: FAIL — `module github_approve_merge.gh_client not found` / attribute errors.

- [ ] **Step 3: Write minimal implementation**

```python
# src/github_approve_merge/gh_client.py
from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass, field
from typing import Callable, Protocol


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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_gh_client.py -q`
Expected: PASS (4 passed).

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/gh_client.py tests/unit/test_gh_client.py
git commit -m "feat(github_approve_merge): add gh_client subprocess seam with typed errors"
```

### Task 2: `GhPR` fetch + auth preflight + merge-queue probe + actions

**Files:**
- Modify: `src/github_approve_merge/gh_client.py`
- Test: `tests/unit/test_gh_client.py`

- [ ] **Step 1: Write the failing tests**

```python
# append to tests/unit/test_gh_client.py
import json as _json

PR_JSON = _json.dumps({
    "number": 565, "state": "OPEN", "isDraft": False, "locked": False,
    "mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN",
    "reviewDecision": "APPROVED",
    "author": {"login": "chkp-muhammady"}, "baseRefName": "master",
    "reviews": [{"author": {"login": "YosiIzaq"}, "state": "APPROVED"}],
})


def test_fetch_pr_parses_fields():
    fake = gc.FakeRunner(stdout=PR_JSON)
    client = gc.GhClient(runner=fake)
    pr = client.fetch_pr("perimeter-81", "platform-global-domain", 565)
    assert pr.state == "OPEN"
    assert pr.mergeable == "MERGEABLE"
    assert pr.review_decision == "APPROVED"
    assert pr.author_login == "chkp-muhammady"
    assert pr.base_ref == "master"
    assert pr.approved_by("YosiIzaq") is True
    assert pr.approved_by("someone-else") is False


def test_current_login():
    fake = gc.FakeRunner(stdout="YosiIzaq\n")
    client = gc.GhClient(runner=fake)
    assert client.current_login() == "YosiIzaq"


def test_has_merge_queue_true_when_node_present():
    fake = gc.FakeRunner(stdout=_json.dumps(
        {"data": {"repository": {"mergeQueue": {"id": "MQ_x"}}}}))
    client = gc.GhClient(runner=fake)
    assert client.has_merge_queue("perimeter-81", "platform-global-domain", "master") is True


def test_has_merge_queue_false_when_null():
    fake = gc.FakeRunner(stdout=_json.dumps(
        {"data": {"repository": {"mergeQueue": None}}}))
    client = gc.GhClient(runner=fake)
    assert client.has_merge_queue("perimeter-81", "platform-global-domain", "master") is False


def test_preflight_ok():
    fake = gc.FakeRunner(stdout="Logged in to github.com account YosiIzaq", returncode=0)
    gc.GhClient(runner=fake).preflight()  # no raise


def test_preflight_raises_auth_when_logged_out():
    fake = gc.FakeRunner(stdout="", stderr="You are not logged into any GitHub hosts", returncode=1)
    with pytest.raises(gc.GhAuthError):
        gc.GhClient(runner=fake).preflight()


def test_enqueue_calls_graphql_mutation():
    fake = gc.FakeRunner(queue=[
        (_json.dumps({"data": {"node": {"id": "PR_x"}}}), "", 0),          # node id
        (_json.dumps({"data": {"enqueuePullRequest": {"mergeQueueEntry": {"state": "QUEUED"}}}}), "", 0),
    ])
    client = gc.GhClient(runner=fake)
    client.enqueue("perimeter-81", "platform-global-domain", 565)
    # second call is the mutation
    assert any("enqueuePullRequest" in " ".join(c) for c in fake.calls)


def test_direct_merge_uses_method_flag():
    fake = gc.FakeRunner(stdout="", returncode=0)
    client = gc.GhClient(runner=fake)
    client.direct_merge("perimeter-81", "repo", 7, method="merge")
    assert fake.calls[-1] == ["gh", "pr", "merge", "7", "--repo",
                              "perimeter-81/repo", "--merge"]


def test_approve_calls_pr_review():
    fake = gc.FakeRunner(returncode=0)
    client = gc.GhClient(runner=fake)
    client.approve("perimeter-81", "repo", 7)
    assert fake.calls[-1] == ["gh", "pr", "review", "7", "--repo",
                              "perimeter-81/repo", "--approve"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_gh_client.py -q`
Expected: FAIL — `GhClient has no attribute fetch_pr` etc.

- [ ] **Step 3: Write minimal implementation**

Append to `gh_client.py`:

```python
# --- GhPR dataclass ---------------------------------------------------------

_PR_FIELDS = "number,state,isDraft,locked,mergeable,mergeStateStatus,reviewDecision,author,baseRefName,reviews"


@dataclass(frozen=True)
class GhPR:
    number: int
    state: str
    is_draft: bool
    locked: bool
    mergeable: str           # MERGEABLE | CONFLICTING | UNKNOWN
    merge_state_status: str  # CLEAN | BLOCKED | BEHIND | DIRTY | UNSTABLE | HAS_HOOKS | DRAFT | UNKNOWN
    review_decision: str     # APPROVED | REVIEW_REQUIRED | CHANGES_REQUESTED | "" (none)
    author_login: str
    base_ref: str
    reviews: list[dict]

    def approved_by(self, login: str) -> bool:
        # Latest review by `login` is APPROVED.
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


# --- GhClient methods (add inside the class) --------------------------------
```

Add these methods to the `GhClient` class:

```python
    def preflight(self) -> None:
        # Raises GhAuthError if gh is not logged in. `gh auth status` exits non-zero when logged out.
        self._run(["auth", "status"])

    def current_login(self) -> str:
        return self._run(["api", "user", "--jq", ".login"]).strip()

    def fetch_pr(self, owner: str, repo: str, number: int) -> GhPR:
        out = self._run([
            "pr", "view", str(number), "--repo", f"{owner}/{repo}",
            "--json", _PR_FIELDS,
        ])
        return GhPR.from_json(out)

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
        flag = {"merge": "--merge", "squash": "--squash", "rebase": "--rebase"}[method]
        self._run(["pr", "merge", str(number), "--repo", f"{owner}/{repo}", flag])

    def enable_auto_merge(self, owner: str, repo: str, number: int, *, method: str) -> None:
        flag = {"merge": "--merge", "squash": "--squash", "rebase": "--rebase"}[method]
        self._run(["pr", "merge", str(number), "--repo", f"{owner}/{repo}", "--auto", flag])

    def approve(self, owner: str, repo: str, number: int) -> None:
        self._run(["pr", "review", str(number), "--repo", f"{owner}/{repo}", "--approve"])
```

Note: `_node_id` is called inside `enqueue`; the test's queued runner returns the node-id JSON first, then the mutation JSON.

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_gh_client.py -q`
Expected: PASS (all).

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/gh_client.py tests/unit/test_gh_client.py
git commit -m "feat(github_approve_merge): gh_client fetch_pr/preflight/queue probe/merge actions"
```

---

## Phase 2 — Classification & merge-action selector

### Task 3: Rewrite `pr_state.py` to classify from `GhPR`

**Files:**
- Modify: `src/github_approve_merge/pr_state.py` (replace DOM logic; keep `PRState`/`StateFlag` enums)
- Test: `tests/unit/test_pr_state_api.py`

- [ ] **Step 1: Write the failing tests**

```python
# tests/unit/test_pr_state_api.py
import pytest
from github_approve_merge.gh_client import GhPR
from github_approve_merge.pr_state import PRState, StateFlag, classify


def mk(**over) -> GhPR:
    base = dict(number=1, state="OPEN", is_draft=False, locked=False,
                mergeable="MERGEABLE", merge_state_status="CLEAN",
                review_decision="APPROVED", author_login="bob",
                base_ref="master", reviews=[])
    base.update(over)
    return GhPR(**base)


@pytest.mark.parametrize("over,expected", [
    (dict(state="MERGED"), PRState.MERGED),
    (dict(state="CLOSED"), PRState.CLOSED),
    (dict(is_draft=True), PRState.DRAFT),
    (dict(locked=True), PRState.LOCKED),
    (dict(author_login="me"), PRState.SELF_AUTHORED),
    (dict(mergeable="CONFLICTING"), PRState.CONFLICT),
    (dict(merge_state_status="BLOCKED", review_decision="APPROVED"), PRState.REQUIRED_FAILING),
    (dict(merge_state_status="BEHIND"), PRState.REQUIRED_PENDING),
    (dict(merge_state_status="UNSTABLE"), PRState.REQUIRED_PENDING),
    (dict(review_decision="REVIEW_REQUIRED", merge_state_status="CLEAN"), PRState.OPEN_APPROVABLE),
    (dict(review_decision="APPROVED", merge_state_status="CLEAN"), PRState.OPEN_MERGEABLE),
])
def test_classify_states(over, expected):
    state, _ = classify(mk(**over), me="me", has_queue=False)
    assert state == expected


def test_self_authored_takes_priority_over_open():
    state, _ = classify(mk(author_login="me", review_decision="REVIEW_REQUIRED"),
                        me="me", has_queue=False)
    assert state == PRState.SELF_AUTHORED


def test_already_approved_flag_set():
    pr = mk(review_decision="APPROVED",
            reviews=[{"author": {"login": "me"}, "state": "APPROVED"}])
    state, flags = classify(pr, me="me", has_queue=False)
    assert StateFlag.ALREADY_APPROVED in flags


def test_unknown_merge_state_is_conservatively_pending():
    state, _ = classify(mk(review_decision="APPROVED", merge_state_status="WEIRD"),
                        me="me", has_queue=False)
    assert state == PRState.REQUIRED_PENDING
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_pr_state_api.py -q`
Expected: FAIL — `cannot import name 'classify'`.

- [ ] **Step 3: Write minimal implementation**

Replace the body of `src/github_approve_merge/pr_state.py` with (keep the `PRState`/`StateFlag` enum definitions exactly as in V1):

```python
from __future__ import annotations

from enum import Enum, auto

from github_approve_merge.gh_client import GhPR


class PRState(Enum):
    MERGED = auto()
    CLOSED = auto()
    DRAFT = auto()
    LOCKED = auto()
    SELF_AUTHORED = auto()
    CONFLICT = auto()
    REQUIRED_FAILING = auto()
    REQUIRED_PENDING = auto()
    OPEN_MERGEABLE = auto()
    OPEN_APPROVABLE = auto()


class StateFlag(Enum):
    ALREADY_APPROVED = auto()


# mergeStateStatus values that mean "checks not done yet" → pending (gated auto-merge/enqueue).
_PENDING_STATUS = {"BEHIND", "UNSTABLE", "HAS_HOOKS", "UNKNOWN"}
# values that mean "blocked on a hard requirement" → failing.
_FAILING_STATUS = {"BLOCKED", "DIRTY"}


def classify(pr: GhPR, *, me: str | None, has_queue: bool) -> tuple[PRState, set[StateFlag]]:
    """Classify a PR from structured gh fields. has_queue informs the action layer, not the
    state — a queue repo still classifies as OPEN_MERGEABLE/REQUIRED_PENDING here."""
    flags: set[StateFlag] = set()

    if pr.state == "MERGED":
        return PRState.MERGED, flags
    if pr.state == "CLOSED":
        return PRState.CLOSED, flags
    if pr.is_draft:
        return PRState.DRAFT, flags
    if pr.locked:
        return PRState.LOCKED, flags
    if me and pr.author_login == me:
        return PRState.SELF_AUTHORED, flags
    if pr.mergeable == "CONFLICTING":
        return PRState.CONFLICT, flags

    if me and pr.approved_by(me):
        flags.add(StateFlag.ALREADY_APPROVED)

    mss = pr.merge_state_status
    if mss in _FAILING_STATUS:
        return PRState.REQUIRED_FAILING, flags
    if mss in _PENDING_STATUS:
        return PRState.REQUIRED_PENDING, flags

    # mss == CLEAN (or DRAFT handled above): decide by review state.
    if pr.review_decision == "APPROVED":
        return PRState.OPEN_MERGEABLE, flags
    return PRState.OPEN_APPROVABLE, flags
```

> Decision detail: `BLOCKED` with an APPROVED review means a *non-review* hard requirement is failing (e.g. a required check) → `REQUIRED_FAILING`. If `review_decision != APPROVED` and `mss == CLEAN`, it's just awaiting our approval → `OPEN_APPROVABLE`.

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_pr_state_api.py -q`
Expected: PASS (all).

- [ ] **Step 5: Delete obsolete enum test and commit**

```bash
git rm tests/unit/test_pr_state_enums.py   # superseded; status/exit-class assertions move to test_actions
git add src/github_approve_merge/pr_state.py tests/unit/test_pr_state_api.py
git commit -m "feat(github_approve_merge): classify PR state from gh API fields"
```

> Note: any status↔exit-class assertions previously in `test_pr_state_enums.py` are re-added in Task 5's `test_actions_status_map`.

### Task 4: `merge_action.py` selector

**Files:**
- Create: `src/github_approve_merge/merge_action.py`
- Test: `tests/unit/test_merge_action.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_merge_action.py
import pytest
from github_approve_merge.pr_state import PRState
from github_approve_merge.merge_action import MergeAction, select_merge_action


@pytest.mark.parametrize("state,has_queue,expected", [
    (PRState.OPEN_MERGEABLE, True, MergeAction.ENQUEUE),
    (PRState.OPEN_MERGEABLE, False, MergeAction.DIRECT_MERGE),
    (PRState.REQUIRED_PENDING, True, MergeAction.ENQUEUE),
    (PRState.REQUIRED_PENDING, False, MergeAction.AUTO_MERGE),
])
def test_select(state, has_queue, expected):
    assert select_merge_action(state, has_queue=has_queue) == expected


def test_non_mergeable_state_raises():
    with pytest.raises(ValueError):
        select_merge_action(PRState.CONFLICT, has_queue=False)
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_merge_action.py -q`
Expected: FAIL — module missing.

- [ ] **Step 3: Write minimal implementation**

```python
# src/github_approve_merge/merge_action.py
from __future__ import annotations

from enum import Enum, auto

from github_approve_merge.pr_state import PRState


class MergeAction(Enum):
    ENQUEUE = auto()        # repo uses a merge queue
    DIRECT_MERGE = auto()   # mergeable now, no queue
    AUTO_MERGE = auto()     # checks pending, no queue → enable auto-merge


_MERGEABLE_STATES = {PRState.OPEN_MERGEABLE, PRState.REQUIRED_PENDING}


def select_merge_action(state: PRState, *, has_queue: bool) -> MergeAction:
    if state not in _MERGEABLE_STATES:
        raise ValueError(f"{state} is not a mergeable state")
    if has_queue:
        return MergeAction.ENQUEUE
    if state is PRState.OPEN_MERGEABLE:
        return MergeAction.DIRECT_MERGE
    return MergeAction.AUTO_MERGE
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_merge_action.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/merge_action.py tests/unit/test_merge_action.py
git commit -m "feat(github_approve_merge): merge-action selector (enqueue/direct/auto)"
```

---

## Phase 3 — Gate & per-PR flow

### Task 5: Status map + `process_pr` over gh_client (no gate yet)

**Files:**
- Modify: `src/github_approve_merge/actions.py`
- Test: `tests/unit/test_process_pr.py` (rewrite), `tests/unit/test_actions_status_map.py` (create)

- [ ] **Step 1: Write the failing status-map test**

```python
# tests/unit/test_actions_status_map.py
from github_approve_merge.actions import STATUS_TO_EXIT_CLASS, ExitClass, aggregate_exit_code, EXIT_CODE_SUCCESS, EXIT_CODE_FAILURE


def test_new_statuses_have_exit_classes():
    assert STATUS_TO_EXIT_CLASS["done"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["queued"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["would-merge"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["skipped-merged"] is ExitClass.SUCCESS
    assert STATUS_TO_EXIT_CLASS["cancelled"] is ExitClass.WARN
    assert STATUS_TO_EXIT_CLASS["failed-auth"] is ExitClass.ERROR
    assert STATUS_TO_EXIT_CLASS["failed-not-found"] is ExitClass.ERROR


def test_aggregate_success_only_when_all_success():
    assert aggregate_exit_code(["done", "queued", "skipped-merged"]) == EXIT_CODE_SUCCESS
    assert aggregate_exit_code(["done", "cancelled"]) == EXIT_CODE_FAILURE
```

- [ ] **Step 2: Write the failing process_pr tests**

```python
# tests/unit/test_process_pr.py  (full rewrite)
import pytest

from github_approve_merge.actions import process_pr, ProcessResult, MergeDecision
from github_approve_merge.gh_client import GhAuthError, GhNotFound
from github_approve_merge.pr_state import PRState, StateFlag
from github_approve_merge.merge_action import MergeAction
from github_approve_merge.url import PRRef


PR = PRRef("perimeter-81", "repo", 1)


class FakeClient:
    """Stand-in for GhClient. Pre-canned classification + records actions."""
    def __init__(self, *, states, has_queue=False, me="me", raise_on_fetch=None):
        self._states = list(states)   # list of (PRState, set[flags])
        self.has_queue_val = has_queue
        self.me = me
        self.raise_on_fetch = raise_on_fetch
        self.approved = False
        self.enqueued = False
        self.direct_merged = False
        self.auto_merged = False
        self.fetches = 0

    # The action layer calls classify_pr(client, pr); we fake that seam by
    # returning canned states. See process_pr signature in Step 4.
    def classify(self, pr):
        if self.raise_on_fetch is not None:
            raise self.raise_on_fetch
        self.fetches += 1
        return self._states.pop(0)

    def has_queue(self, pr):
        return self.has_queue_val

    def approve(self, pr):
        self.approved = True

    def enqueue(self, pr):
        self.enqueued = True

    def direct_merge(self, pr, method):
        self.direct_merged = True

    def enable_auto_merge(self, pr, method):
        self.auto_merged = True


def always_yes(_decisions):  # gate that approves the plan
    return [True] * len(_decisions)


@pytest.mark.asyncio
async def test_merged_skips():
    c = FakeClient(states=[(PRState.MERGED, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "skipped-merged"
    assert not c.enqueued and not c.direct_merged


@pytest.mark.asyncio
async def test_open_mergeable_direct_merge():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())], has_queue=False)
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "done"
    assert c.direct_merged and not c.approved


@pytest.mark.asyncio
async def test_open_mergeable_enqueue_on_queue_repo():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())], has_queue=True)
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "queued"
    assert c.enqueued


@pytest.mark.asyncio
async def test_approvable_then_mergeable_approves_then_enqueues():
    c = FakeClient(states=[(PRState.OPEN_APPROVABLE, set()),
                           (PRState.OPEN_MERGEABLE, set())], has_queue=True)
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert c.approved and c.enqueued
    assert r.status == "queued"


@pytest.mark.asyncio
async def test_approvable_still_approvable_needs_more():
    c = FakeClient(states=[(PRState.OPEN_APPROVABLE, set()),
                           (PRState.OPEN_APPROVABLE, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "skipped-needs-more-approvals"
    assert c.approved and not c.direct_merged


@pytest.mark.asyncio
async def test_gate_decline_records_cancelled():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge",
                         gate=lambda decisions: [False])
    assert r.status == "cancelled"
    assert not c.direct_merged


@pytest.mark.asyncio
async def test_dry_run_reports_would_merge_no_action():
    c = FakeClient(states=[(PRState.OPEN_MERGEABLE, set())])
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge",
                         gate=always_yes, dry_run=True)
    assert r.status == "would-merge"
    assert not c.direct_merged and not c.approved


@pytest.mark.asyncio
async def test_auth_error_records_failed_auth():
    c = FakeClient(states=[], raise_on_fetch=GhAuthError("sso"))
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "failed-auth"


@pytest.mark.asyncio
async def test_not_found_records_failed_not_found():
    c = FakeClient(states=[], raise_on_fetch=GhNotFound("404"))
    r = await process_pr(c, PR, approve=True, do_merge=True, method="merge", gate=always_yes)
    assert r.status == "failed-not-found"
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `uv run pytest tests/unit/test_process_pr.py tests/unit/test_actions_status_map.py -q`
Expected: FAIL — `process_pr`/`MergeDecision` signatures don't exist yet.

- [ ] **Step 4: Write minimal implementation**

Rewrite `src/github_approve_merge/actions.py`:

```python
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from enum import Enum
from typing import Callable

from github_approve_merge.gh_client import GhAuthError, GhError, GhNotFound
from github_approve_merge.merge_action import MergeAction, select_merge_action
from github_approve_merge.pr_state import PRState, StateFlag, classify
from github_approve_merge.url import PRRef

EXIT_CODE_SUCCESS = 0
EXIT_CODE_FAILURE = 1
EXIT_CODE_USAGE = 2
EXIT_CODE_INTERRUPTED = 130

_log = logging.getLogger("gam")


class ExitClass(Enum):
    SUCCESS = "success"
    WARN = "warn"
    ERROR = "error"


STATUS_TO_EXIT_CLASS: dict[str, ExitClass] = {
    "done": ExitClass.SUCCESS,
    "queued": ExitClass.SUCCESS,
    "would-merge": ExitClass.SUCCESS,
    "skipped-merged": ExitClass.SUCCESS,
    "skipped-closed": ExitClass.WARN,
    "skipped-draft": ExitClass.WARN,
    "skipped-self": ExitClass.WARN,
    "skipped-needs-more-approvals": ExitClass.WARN,
    "cancelled": ExitClass.WARN,
    "failed-conflict": ExitClass.ERROR,
    "failed-required-check": ExitClass.ERROR,
    "failed-locked": ExitClass.ERROR,
    "failed-auth": ExitClass.ERROR,
    "failed-not-found": ExitClass.ERROR,
    "failed-interrupted": ExitClass.ERROR,
    "failed-exception": ExitClass.ERROR,
}


def aggregate_exit_code(statuses: list[str]) -> int:
    if not statuses:
        return EXIT_CODE_FAILURE
    for s in statuses:
        cls = STATUS_TO_EXIT_CLASS.get(s)
        if cls is None or cls is not ExitClass.SUCCESS:
            return EXIT_CODE_FAILURE
    return EXIT_CODE_SUCCESS


_STATE_TO_TERMINAL_STATUS: dict[PRState, str] = {
    PRState.MERGED: "skipped-merged",
    PRState.CLOSED: "skipped-closed",
    PRState.DRAFT: "skipped-draft",
    PRState.SELF_AUTHORED: "skipped-self",
    PRState.CONFLICT: "failed-conflict",
    PRState.REQUIRED_FAILING: "failed-required-check",
    PRState.LOCKED: "failed-locked",
}
_TERMINAL_STATES = set(_STATE_TO_TERMINAL_STATUS)
_MERGEABLE_STATES = {PRState.OPEN_MERGEABLE, PRState.REQUIRED_PENDING}


@dataclass(frozen=True)
class ProcessResult:
    status: str
    error_message: str = ""
    duration_ms: int = 0


@dataclass(frozen=True)
class MergeDecision:
    pr: PRRef
    state: PRState
    action: MergeAction
    will_approve: bool


# Gate: given the list of MergeDecisions, return a parallel list of bools (proceed?).
Gate = Callable[[list[MergeDecision]], list[bool]]


async def process_pr(
    client,
    pr: PRRef,
    *,
    approve: bool,
    do_merge: bool,
    method: str,
    gate: Gate,
    dry_run: bool = False,
) -> ProcessResult:
    started = time.monotonic()
    try:
        state, flags = client.classify(pr)

        if state in _TERMINAL_STATES:
            return _result(_STATE_TO_TERMINAL_STATUS[state], started)

        # Approve step (if needed and requested).
        will_approve = (
            approve and state is PRState.OPEN_APPROVABLE
            and StateFlag.ALREADY_APPROVED not in flags
        )

        if dry_run:
            return _result("would-merge", started)

        if will_approve:
            client.approve(pr)
            state, flags = client.classify(pr)
            if state in _TERMINAL_STATES:
                return _result(_STATE_TO_TERMINAL_STATUS[state], started)
            if state is PRState.OPEN_APPROVABLE:
                return _result("skipped-needs-more-approvals", started)

        if not do_merge or state not in _MERGEABLE_STATES:
            return _result("skipped-needs-more-approvals", started)

        action = select_merge_action(state, has_queue=client.has_queue(pr))
        decision = MergeDecision(pr=pr, state=state, action=action, will_approve=will_approve)

        # Gate: single-PR path here; batch gating handled by the runner (Task 6).
        if not gate([decision])[0]:
            return _result("cancelled", started)

        if action is MergeAction.ENQUEUE:
            client.enqueue(pr)
            return _result("queued", started)
        if action is MergeAction.DIRECT_MERGE:
            client.direct_merge(pr, method)
            return _result("done", started)
        client.enable_auto_merge(pr, method)
        return _result("done", started)

    except GhAuthError as e:
        return ProcessResult("failed-auth", repr(e), _elapsed(started))
    except GhNotFound as e:
        return ProcessResult("failed-not-found", repr(e), _elapsed(started))
    except Exception as e:  # broad: batch must continue
        _log.error("process_pr failed", exc_info=True, extra={"pr": str(pr)})
        return ProcessResult("failed-exception", repr(e), _elapsed(started))


def _result(status: str, started: float) -> ProcessResult:
    return ProcessResult(status=status, duration_ms=_elapsed(started))


def _elapsed(started: float) -> int:
    return int((time.monotonic() - started) * 1000)
```

> The `FakeClient` in the test provides `classify`/`has_queue`/`approve`/`enqueue`/`direct_merge`/`enable_auto_merge`. The real `GhClient` is adapted to this shape in Task 6 (a tiny `PrClient` wrapper binds owner/repo/number so `process_pr` stays PR-centric).

- [ ] **Step 5: Run tests to verify they pass**

Run: `uv run pytest tests/unit/test_process_pr.py tests/unit/test_actions_status_map.py -q`
Expected: PASS (all).

- [ ] **Step 6: Commit**

```bash
git add src/github_approve_merge/actions.py tests/unit/test_process_pr.py tests/unit/test_actions_status_map.py
git commit -m "feat(github_approve_merge): process_pr over gh client with merge gate + new statuses"
```

### Task 6: Gate UI + `PrClient` adapter

**Files:**
- Create: `src/github_approve_merge/gate.py`
- Test: `tests/unit/test_gate.py`

- [ ] **Step 1: Write the failing test**

```python
# tests/unit/test_gate.py
import io
from github_approve_merge.actions import MergeDecision
from github_approve_merge.merge_action import MergeAction
from github_approve_merge.pr_state import PRState
from github_approve_merge.url import PRRef
from github_approve_merge.gate import render_plan, make_gate


D = [MergeDecision(PRRef("o", "r", 5), PRState.OPEN_MERGEABLE, MergeAction.ENQUEUE, False),
     MergeDecision(PRRef("o", "r", 6), PRState.OPEN_APPROVABLE, MergeAction.DIRECT_MERGE, True)]


def test_render_plan_lists_each_pr_and_action():
    text = render_plan(D)
    assert "o/r#5" in text and "enqueue" in text
    assert "o/r#6" in text and "approve" in text and "direct" in text


def test_yes_gate_auto_approves():
    gate = make_gate(assume_yes=True, confirm_each=False, stream=io.StringIO())
    assert gate(D) == [True, True]


def test_interactive_gate_reads_yes(monkeypatch):
    out = io.StringIO()
    monkeypatch.setattr("builtins.input", lambda *_: "y")
    gate = make_gate(assume_yes=False, confirm_each=False, stream=out)
    assert gate(D) == [True, True]
    assert "Proceed with merge for 2" in out.getvalue()


def test_interactive_gate_reads_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda *_: "")
    gate = make_gate(assume_yes=False, confirm_each=False, stream=io.StringIO())
    assert gate(D) == [False, False]


def test_confirm_each(monkeypatch):
    answers = iter(["y", "n"])
    monkeypatch.setattr("builtins.input", lambda *_: next(answers))
    gate = make_gate(assume_yes=False, confirm_each=True, stream=io.StringIO())
    assert gate(D) == [True, False]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_gate.py -q`
Expected: FAIL — module missing.

- [ ] **Step 3: Write minimal implementation**

```python
# src/github_approve_merge/gate.py
from __future__ import annotations

import sys
from typing import TextIO

from github_approve_merge.actions import MergeDecision
from github_approve_merge.merge_action import MergeAction

_ACTION_LABEL = {
    MergeAction.ENQUEUE: "enqueue (merge queue)",
    MergeAction.DIRECT_MERGE: "direct merge",
    MergeAction.AUTO_MERGE: "enable auto-merge",
}


def _slug(d: MergeDecision) -> str:
    return f"{d.pr.owner}/{d.pr.repo}#{d.pr.number}"


def render_plan(decisions: list[MergeDecision]) -> str:
    lines = ["", "Merge plan:"]
    for d in decisions:
        prefix = "approve → " if d.will_approve else ""
        lines.append(f"  {_slug(d):<48} {d.state.name:<16} {prefix}{_ACTION_LABEL[d.action]}")
    return "\n".join(lines)


def make_gate(*, assume_yes: bool, confirm_each: bool, stream: TextIO = sys.stderr):
    def gate(decisions: list[MergeDecision]) -> list[bool]:
        if assume_yes:
            return [True] * len(decisions)
        if confirm_each:
            out = []
            for d in decisions:
                print(render_plan([d]), file=stream)
                ans = input(f"Merge {_slug(d)}? [y/N]: ").strip().lower()
                out.append(ans in ("y", "yes"))
            return out
        print(render_plan(decisions), file=stream)
        ans = input(f"Proceed with merge for {len(decisions)} PR(s)? [y/N]: ").strip().lower()
        return [ans in ("y", "yes")] * len(decisions)
    return gate
```

- [ ] **Step 4: Run test to verify it passes**

Run: `uv run pytest tests/unit/test_gate.py -q`
Expected: PASS.

- [ ] **Step 5: Add the `PrClient` adapter to gh_client.py**

Append to `src/github_approve_merge/gh_client.py`:

```python
@dataclass
class PrClient:
    """Binds a GhClient + PRRef-ish coordinates so process_pr can stay PR-centric.
    Caches the merge-queue probe and authenticated login across the per-PR flow."""
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
```

- [ ] **Step 6: Add adapter test + run**

```python
# append to tests/unit/test_gh_client.py
def test_prclient_classify_caches_queue_probe():
    fake = gc.FakeRunner(queue=[
        (PR_JSON, "", 0),                                                # fetch_pr #1
        (_json.dumps({"data": {"repository": {"mergeQueue": {"id": "x"}}}}), "", 0),  # queue probe
        (PR_JSON, "", 0),                                                # fetch_pr #2
    ])
    pc = gc.PrClient(gh=gc.GhClient(runner=fake), owner="o", repo="r", number=565, me="YosiIzaq")
    pc.classify(None)
    pc.classify(None)            # second classify must NOT re-probe the queue
    probe_calls = [c for c in fake.calls if "mergeQueue" in " ".join(c)]
    assert len(probe_calls) == 1
    assert pc.has_queue(None) is True
```

Run: `uv run pytest tests/unit/test_gate.py tests/unit/test_gh_client.py -q`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/github_approve_merge/gate.py src/github_approve_merge/gh_client.py tests/unit/test_gate.py tests/unit/test_gh_client.py
git commit -m "feat(github_approve_merge): merge-plan gate UI + PrClient adapter"
```

---

## Phase 4 — Runner, CLI, config

### Task 7: Runner threads gate + batch confirmation

**Files:**
- Modify: `src/github_approve_merge/runner.py`
- Test: `tests/unit/test_runner.py` (extend)

- [ ] **Step 1: Read the current runner to preserve its resume/state.jsonl/summary contract**

Run: `sed -n '1,200p' src/github_approve_merge/runner.py`
Expected: understand `run_batch` signature, how it builds page objects today, where `process_pr` is called, and how `state.jsonl`/`summary.json` are written.

- [ ] **Step 2: Write the failing test**

```python
# append to tests/unit/test_runner.py
import pytest
from github_approve_merge.runner import run_batch
from github_approve_merge.url import PRRef


class StubClientFactory:
    """Returns a FakeClient-like per PR. Records that batch gate was passed in."""
    def __init__(self, status_by_number):
        self.status_by_number = status_by_number
        self.built = []

    def __call__(self, pr: PRRef, me: str):
        self.built.append(pr.number)
        num = pr.number
        from tests.unit.test_process_pr import FakeClient
        from github_approve_merge.pr_state import PRState
        return FakeClient(states=[(PRState.OPEN_MERGEABLE, set())],
                          has_queue=(num % 2 == 0))


@pytest.mark.asyncio
async def test_run_batch_collects_plan_then_gates_once(tmp_path):
    prs = [PRRef("o", "r", 1), PRRef("o", "r", 2)]
    gate_calls = []

    def gate(decisions):
        gate_calls.append(len(decisions))
        return [True] * len(decisions)

    summary = await run_batch(
        prs, client_factory=StubClientFactory({}), me="me",
        approve=True, do_merge=True, method="merge",
        gate=gate, logs_dir=tmp_path, run_id="rid",
    )
    # Plan-collection means the gate sees both PRs at once (batch confirmation).
    assert gate_calls == [2]
    assert summary["counts"]["queued"] + summary["counts"]["done"] == 2
```

- [ ] **Step 3: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_runner.py -q`
Expected: FAIL — `run_batch` new signature not present.

- [ ] **Step 4: Implement the two-pass batch in runner.py**

Modify `run_batch` to: (1) build a `PrClient` per PR via `client_factory`; (2) **pass 1** — call a classify+plan function for each PR that returns either a terminal `ProcessResult` (recorded immediately) or a `MergeDecision`; (3) call `gate(all_decisions)` **once**; (4) **pass 2** — execute each gated decision, writing `state.jsonl` transitions and `summary.json` exactly as V1 did. Reuse existing log/summary writers. For dry-run, skip the gate and record `would-merge` in pass 1.

Key shape (the engineer adapts to the existing writers):

```python
async def run_batch(prs, *, client_factory, me, approve, do_merge, method, gate,
                    logs_dir, run_id, dry_run=False, resume_done=frozenset()):
    results: dict[int, ProcessResult] = {}
    decisions = []
    for pr in prs:
        if pr.number in resume_done:
            continue
        client = client_factory(pr, me)
        # Reuse process_pr for terminal/dry-run/approve paths but stop before the gate by
        # passing a "defer" gate that raises a sentinel carrying the MergeDecision.
        ...
    proceed = gate(decisions) if (decisions and not dry_run) else [True] * len(decisions)
    ...
    return summary
```

> Implementation note: the cleanest factoring is to split `process_pr` into `plan_pr(client, pr, ...)` → `ProcessResult | MergeDecision` and `execute_decision(client, decision, method)` → `ProcessResult`, then have the single-PR `process_pr` (Task 5) call both with an inline gate. Refactor Task 5's body into these two helpers and keep `process_pr` as the thin single-PR wrapper so its tests still pass. Update `tests/unit/test_process_pr.py` only if a helper name is asserted (it is not).

- [ ] **Step 5: Run tests**

Run: `uv run pytest tests/unit/test_runner.py tests/unit/test_process_pr.py -q`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/github_approve_merge/runner.py src/github_approve_merge/actions.py tests/unit/test_runner.py
git commit -m "feat(github_approve_merge): two-pass batch runner with single gate"
```

### Task 8: CLI verbs

**Files:**
- Modify: `src/github_approve_merge/cli.py`, `src/github_approve_merge/config.py`
- Test: `tests/unit/test_cli.py`

- [ ] **Step 1: Write the failing tests**

```python
# additions to tests/unit/test_cli.py
import pytest
from github_approve_merge.cli import build_parser


def test_parser_has_new_verbs():
    p = build_parser()
    # argparse subparsers are in the _subparsers action
    sub = [a for a in p._actions if a.dest == "command"][0]
    assert set(sub.choices) >= {"auth", "approve", "merge", "run", "gc"}


def test_run_accepts_merge_method_and_yes():
    p = build_parser()
    ns = p.parse_args(["run", "--merge-method", "squash", "--yes",
                       "https://github.com/o/r/pull/1"])
    assert ns.merge_method == "squash"
    assert ns.yes is True


def test_merge_method_default_is_merge():
    p = build_parser()
    ns = p.parse_args(["merge", "https://github.com/o/r/pull/1"])
    assert ns.merge_method == "merge"


def test_no_auth_login_subcommand():
    p = build_parser()
    with pytest.raises(SystemExit):
        p.parse_args(["auth", "login"])   # login removed; only `status`
```

- [ ] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/unit/test_cli.py -q`
Expected: FAIL — old parser still has `auth login`, no `--merge-method`.

- [ ] **Step 3: Implement**

In `cli.py`: build subparsers `auth` (only `status`, alias `doctor` as a top-level subcommand too), `approve`, `merge`, `run`, `gc`. Shared options helper applied to approve/merge/run: positional `urls`, `--file`, `--dry-run`, `--merge-method {merge,squash,rebase}` default `merge`, `--yes`, `--confirm-each`, `--resume`, `--redact-logs`, `--retention-days`, `--logs-dir`, `--run-id`, `--verbose`/`--quiet`. `run` also gets `--no-approve`. The dispatch:
- `auth status`/`doctor` → `GhClient().preflight()` then print `gh auth status`; on `GhAuthError` print actionable message, exit ERROR.
- `approve` → `run` with `do_merge=False`.
- `merge` → `run` with `approve=False`.
- `run` → preflight, read inputs (`input_sources`), build `gate = make_gate(assume_yes=ns.yes, confirm_each=ns.confirm_each)`, call `run_batch(...)`, print summary, exit `aggregate_exit_code`.

In `config.py`: remove `storage_state`/`headless` fields; keep `logs_dir`, `retention_days`, `redact_logs`, `run_id`.

- [ ] **Step 4: Run tests**

Run: `uv run pytest tests/unit/test_cli.py -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/github_approve_merge/cli.py src/github_approve_merge/config.py tests/unit/test_cli.py
git commit -m "feat(github_approve_merge): CLI verbs approve/merge/run + auth status/doctor"
```

### Task 9: Full suite + live smoke rewrite

**Files:**
- Modify: `tests/live/test_smoke.py`
- Create: `tests/fixtures/json/pr_open_mergeable.json` (sanitized real capture)

- [ ] **Step 1: Rewrite the live smoke (read-only)**

```python
# tests/live/test_smoke.py
import os
import pytest
from github_approve_merge.gh_client import GhClient

pytestmark = pytest.mark.skipif(os.environ.get("PYTEST_LIVE") != "1",
                                reason="PYTEST_LIVE=1 not set")


def test_live_fetch_pr_readonly():
    gh = GhClient()
    gh.preflight()
    pr = gh.fetch_pr("perimeter-81", "platform-global-domain", 565)
    assert pr.number == 565
    assert pr.state in {"OPEN", "MERGED", "CLOSED"}
```

- [ ] **Step 2: Run the full suite**

Run: `uv run pytest -q`
Expected: all unit + fixture tests PASS; live smoke SKIPPED.

- [ ] **Step 3: Type/lint check (match existing config)**

Run: `uv run mypy src/github_approve_merge` (if mypy configured) — fix real type errors only.
Expected: clean (or no new errors vs baseline).

- [ ] **Step 4: Commit**

```bash
git add tests/live/test_smoke.py tests/fixtures/json/
git commit -m "test(github_approve_merge): read-only gh live smoke + json fixtures"
```

---

## Phase 5 — Docs, version, integrations

### Task 10: README + CHANGELOG + version bump

**Files:**
- Modify: `README.md`, `CHANGELOG.md`, `pyproject.toml` (version → `0.2.0`)

- [ ] **Step 1: Rewrite README prerequisites & exit codes**

Replace the `auth login` / `storage_state` prose with: prerequisite "`gh` installed and `gh auth login` (token SSO-authorized for the org)"; document `approve`/`merge`/`run`, the merge gate + `--yes`/`--confirm-each`, `--merge-method`, and the new exit-code row (add `queued`, `would-merge` to success; `cancelled` to warn). Remove the Playwright/selector troubleshooting; add a `failed-auth` troubleshooting row pointing at `gh auth status` / SSO authorization.

- [ ] **Step 2: CHANGELOG `0.2.0` entry**

```markdown
## [0.2.0] - 2026-06-01

### Changed (breaking)
- Backend swapped from Playwright/storage_state to the GitHub API via the `gh` CLI.
- Removed `auth login` (no browser). Prereq is now `gh auth login` (SSO-authorized token).
- New verbs: `approve`, `merge`, `run`; `merge`/`run` require confirmation (merge gate)
  unless `--yes`. `--merge-method` (default `merge`). `--confirm-each` for per-PR gating.

### Added
- Auto-detected merge action: enqueue (merge queue) / direct merge / enable auto-merge.
- `auth status` / `doctor` checks `gh` + login + SSO authorization.
- Statuses `queued`, `cancelled`; dry-run reports `would-merge`.

### Removed
- Playwright dependency, browser/page-object code, screenshots, HTML fixtures.
```

- [ ] **Step 3: Bump version**

Edit `pyproject.toml`: `version = "0.2.0"`.

- [ ] **Step 4: Full suite sanity + commit**

Run: `uv run pytest -q`
Expected: PASS / live SKIPPED.

```bash
git add README.md CHANGELOG.md pyproject.toml
git commit -m "docs(github_approve_merge): v0.2.0 API-backend README/CHANGELOG + version bump"
```

### Task 11: Wire `launcher.sh` submenu

**Files:**
- Modify: `/Users/yosii/work/git/personal_code/code/bash/launcher.sh` (`show_github_merger_menu` + `handle_github_merger_menu`, lines ~1603–1751)

- [ ] **Step 1: Replace the submenu display**

Update `show_github_merger_menu` items to:
```
[1] Doctor (gh + SSO)
[2] Dry-Run (plan)
[3] Approve only
[4] Merge (gated)
[5] Run = approve + merge (gated)
[6] Cleanup Old Logs (GC)
[0] Back
```
Update the prompt to `[0-6]`.

- [ ] **Step 2: Replace the handler cases**

In `handle_github_merger_menu`, remove the `GITHUB_MERGER_VENV` reference and the browser-login case. Keep the `uv`/dir guards. New cases (reuse the existing input sub-prompt + `--redact-logs` prompt for 2–5):
```bash
1) cd "$GITHUB_MERGER_DIR"; uv run gh-approve-merge auth status; cd - >/dev/null ;;
2) ... gather input ...; uv run gh-approve-merge run --dry-run $redact_flag $extra_args ;;
3) ... gather input ...; uv run gh-approve-merge approve $redact_flag $extra_args ;;
4) ... gather input ...; uv run gh-approve-merge merge $redact_flag $extra_args ;;   # tool prompts [y/N]
5) ... gather input ...; uv run gh-approve-merge run $redact_flag $extra_args ;;       # tool prompts [y/N]
6) cd "$GITHUB_MERGER_DIR"; uv run gh-approve-merge gc; cd - >/dev/null ;;
```
Do **not** pass `--yes` — the gate must prompt interactively.

- [ ] **Step 3: Syntax-check the launcher**

Run: `bash -n /Users/yosii/work/git/personal_code/code/bash/launcher.sh`
Expected: no output (syntax OK).

- [ ] **Step 4: Commit (launcher lives in the same repo, different path)**

```bash
cd /Users/yosii/work/git/personal_code
git add code/bash/launcher.sh
git commit -m "feat(launcher): point GitHub PR Merger submenu at gh-approve-merge v0.2 verbs"
cd automations/github_approve_merge
```

### Task 12: Wire `pr_reviewer_agent.md` handoff

**Files:**
- Modify: `/Users/yosii/work/CheckPoint/agents/pr_reviewer_agent.md`

- [ ] **Step 1: Add a "Handoff to merger" section near the Final Verdict (~line 412)**

Insert content stating, verbatim intent:
- Hard rule: **the reviewer agent never approves and never merges.** It outputs a verdict only.
- On an "Approved for merge" verdict, and only with the human's explicit go-ahead, write the reviewed PR URL(s) to a list file, then surface:
  `cd /Users/yosii/work/git/personal_code/automations/github_approve_merge && uv run gh-approve-merge merge --file <list>` (or `run` to also submit the approval). The command runs behind the tool's confirmation gate — the human confirms `[y/N]`.
- Note batch friendliness: multiple reviewed PRs flow into one gated merge.

- [ ] **Step 2: Update the agent's changelog/footer**

Add a dated line to the agent doc's revision log: `Added "Handoff to merger" — agent never merges; emits gated gh-approve-merge command.`

- [ ] **Step 3: Commit**

```bash
cd /Users/yosii/work/CheckPoint
git add agents/pr_reviewer_agent.md
git commit -m "docs(pr-reviewer): add gated handoff to gh-approve-merge (agent never merges)"
cd /Users/yosii/work/git/personal_code/automations/github_approve_merge
```

> Note: if `/Users/yosii/work/CheckPoint` is not a git repo or is a different remote, skip the commit and just save the file; report that to the user.

---

## Self-Review

**Spec coverage:**
- §4.1 replace Playwright → Task 0 (delete) + all of Phase 1–4. ✓
- §4.2 shell out to gh → Task 1–2 (`gh_client`). ✓
- §4.3 auto-detect merge → Task 4 (`merge_action`) + Task 5 execution. ✓
- §4.4 method default merge + fallback → Task 8 (`--merge-method` default merge); fallback-if-disallowed is logged in `direct_merge` — **gap:** add fallback in Task 2 impl note. (See fix below.)
- §4.5 merge gate (plan, `--yes`, `--confirm-each`, dry-run no gate) → Task 6 + Task 7. ✓
- §4.6 verbs approve/merge/run + `--no-approve` → Task 8. ✓
- §4.7 classification → Task 3. ✓
- §4.8 preflight/doctor → Task 2 (`preflight`) + Task 8 (`auth status`/`doctor`). ✓
- §4.9 JSONL logs/summary kept → Task 7 reuses V1 writers. ✓
- §4.10 resume/redact/retention → Task 7 (`resume_done`), Task 8 (flags), `retention.py` kept. ✓
- §4.11 dry-run `would-merge` → Task 5. ✓
- §6 classifier mapping → Task 3 tests cover every row. ✓
- §7 statuses/exit classes incl. `queued`/`cancelled` → Task 5. ✓
- §9.1 launcher → Task 11. §9.2 agent → Task 12. ✓
- §10 testing → fakes throughout, json fixtures Task 9. ✓
- §11 version/README/CHANGELOG → Task 10. ✓

**Gap fix (§4.4 method fallback):** In Task 2, `direct_merge` should fall back to an allowed method if the requested one is disabled. Add to the `direct_merge` impl: catch `GhError` whose stderr mentions the method is not allowed, query `gh api repos/{o}/{r} --jq '{m:.allow_merge_commit,s:.allow_squash_merge,b:.allow_rebase_merge}'`, pick the first allowed in order merge→squash→rebase, log the substitution, retry once. Add a test in `test_gh_client.py` using a queued `FakeRunner` (first call fails "Merge commits are not allowed", second call is the repo query, third is the retry) asserting the retry uses an allowed flag.

**Placeholder scan:** No TBD/TODO; every code step has complete code except Task 7-step-4 and Task 11/12 which describe edits to large existing files (launcher.sh, runner.py, agent md) — these reference exact functions/line ranges and show the case bodies, which is the appropriate granularity for editing big existing files.

**Type consistency:** `classify(pr, *, me, has_queue)` used identically in Task 3 tests, Task 5 `process_pr`, and Task 6 `PrClient`. `MergeAction.{ENQUEUE,DIRECT_MERGE,AUTO_MERGE}` consistent across Tasks 4/5/6. `MergeDecision(pr,state,action,will_approve)` consistent Tasks 5/6/7. Client method names (`classify`,`has_queue`,`approve`,`enqueue`,`direct_merge`,`enable_auto_merge`) identical in `FakeClient` (Task 5) and `PrClient` (Task 6). ✓
