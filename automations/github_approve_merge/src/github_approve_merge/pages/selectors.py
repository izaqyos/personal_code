"""Central registry of every selector used by Page Objects.

When GitHub redesigns and tests start failing, this is the single file to update.

Prefer role + accessible name (regex). Fall back to data-* attributes. Use CSS
class only as a last resort and explain why in a comment next to the constant.
"""
from __future__ import annotations

import re

# --- Review submission form (FilesPage) -------------------------------------

APPROVE_RADIO_VALUE = "approve"  # name="pull_request_review[event]", value="approve"
SUBMIT_REVIEW_NAME = re.compile(r"^Submit review$")

# --- Merge box (PRPage) -----------------------------------------------------

MERGE_BUTTON_NAME = re.compile(
    r"^(Merge pull request|Create a merge commit|Squash and merge|Rebase and merge)$"
)
CONFIRM_MERGE_NAME = re.compile(
    r"^Confirm (merge|squash and merge|rebase and merge)$"
)
MERGE_WHEN_READY_NAME = re.compile(r"^Merge when ready$")
ENABLE_AUTO_MERGE_NAME = re.compile(r"^Enable auto-merge$")  # alternative copy GitHub uses

# --- Identity ---------------------------------------------------------------

USER_LOGIN_META = 'meta[name="user-login"]'  # `content=<login>` on every github.com page

# --- Status badges and notices (used by detect_state) -----------------------

STATE_BADGE_MERGED = re.compile(r"^Merged$")          # role=status/title in header
STATE_BADGE_CLOSED = re.compile(r"^Closed$")
DRAFT_BADGE_TEXT = re.compile(r"^Draft$")
LOCKED_NOTICE_TEXT = re.compile(r"This conversation has been locked", re.I)
CONFLICT_NOTICE_TEXT = re.compile(r"This branch has conflicts", re.I)
REQUIRED_STATUS_TEXT = re.compile(r"Required statuses must pass", re.I)

# --- Reviewers panel --------------------------------------------------------

REVIEWERS_PANEL_APPROVED_LABEL = re.compile(r"approved these changes", re.I)

# CSS fallback used by PR-author lookup. The accessible-name path is the
# author link's text in the PR header timeline; this CSS hook is the
# resilient identifier (data-hovercard-type=user inside .timeline-comment-header
# for the PR opening comment).
PR_AUTHOR_LINK_CSS = '.gh-header-meta a.author[data-hovercard-type="user"]'
