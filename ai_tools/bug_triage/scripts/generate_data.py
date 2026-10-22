"""Deterministic generator for the INVENTED Larkspur data set.

Usage: python scripts/generate_data.py [--out DIR]
Everything written here is fictional: no real companies, products or people.
"""

from __future__ import annotations

import argparse
import json
import random
import string
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

import yaml

DEFAULT_OUT = Path(__file__).resolve().parents[1] / "data"

TEAMS: dict[str, dict[str, Any]] = {
    "Identity": {
        "members": ["Tobias Wren", "Priya Anand", "Marcus Oyelaran", "Hana Lindqvist"],
        "components": ["auth-sso", "public-api", "permissions"],
    },
    "Payments": {
        "members": ["Dmitri Volkov", "Amara Okafor", "Julian Reyes"],
        "components": ["billing", "reporting"],
    },
    "Platform": {
        "members": ["Sofia Marchetti", "Kwame Boateng", "Ingrid Halvorsen", "Rahul Deshpande"],
        "components": ["sync-engine", "file-storage", "search"],
    },
    "Experience": {
        "members": ["Yuki Tanabe", "Camille Durand", "Oskar Nilsson"],
        "components": ["web-ui", "mobile-app", "notifications"],
    },
}

COMPONENTS: dict[str, dict[str, Any]] = {
    "auth-sso": {
        "assignee": "Tobias Wren",
        "keywords": ["login", "sso", "saml", "session", "mfa", "password", "idp", "sign-in"],
    },
    "public-api": {
        "assignee": "Priya Anand",
        "keywords": ["api", "endpoint", "token", "rate limit", "webhook", "rest", "gateway"],
    },
    "permissions": {
        "assignee": "Marcus Oyelaran",
        "keywords": ["permission", "role", "access denied", "403", "scope", "guest", "group"],
    },
    "billing": {
        "assignee": "Dmitri Volkov",
        "keywords": ["invoice", "payment", "card", "tax", "subscription", "plan", "coupon"],
    },
    "reporting": {
        "assignee": "Amara Okafor",
        "keywords": ["report", "dashboard", "chart", "csv", "export", "burndown", "velocity"],
    },
    "sync-engine": {
        "assignee": "Sofia Marchetti",
        "keywords": ["sync", "conflict", "offline", "merge", "cursor", "tombstone", "replica"],
    },
    "file-storage": {
        "assignee": "Kwame Boateng",
        "keywords": ["upload", "download", "attachment", "zip", "quota", "thumbnail", "export"],
    },
    "search": {
        "assignee": "Ingrid Halvorsen",
        "keywords": ["search", "index", "query", "autocomplete", "results", "filter", "ranking"],
    },
    "web-ui": {
        "assignee": "Yuki Tanabe",
        "keywords": ["button", "page", "layout", "dark mode", "browser", "drag", "render", "ui"],
    },
    "mobile-app": {
        "assignee": "Camille Durand",
        "keywords": ["app", "ios", "android", "crash", "push", "biometric", "mobile", "login"],
    },
    "notifications": {
        "assignee": "Oskar Nilsson",
        "keywords": ["notification", "email", "digest", "push", "mention", "unsubscribe", "alert"],
    },
}

# (id, component, title, symptoms, workaround, status, log, alternative wording)
KNOWN_ISSUES: list[tuple[str, str, str, str, str, str, str, str]] = [
    (
        "KI-001",
        "auth-sso",
        "SSO login loops when third-party cookies are blocked",
        "Login through the corporate IdP bounces between /login and /sso/callback when the "
        "browser blocks third-party cookies.",
        "Allow cookies for the Larkspur domain or use the direct sign-in link.",
        "open",
        "ERROR auth.sso callback: state cookie missing, restarting login flow",
        "Users cannot get past sign-in, the page keeps redirecting back to the SSO callback "
        "and the state cookie is never stored.",
    ),
    (
        "KI-002",
        "auth-sso",
        "SAML metadata rotation invalidates active sessions",
        "After the IdP rotates its signing certificate every active session is dropped and "
        "login fails with an audience or signature error until metadata is refreshed.",
        "Re-upload the IdP metadata in SSO settings.",
        "fixed",
        "ERROR auth.saml: signature validation failed kid=rotated",
        "Everybody got logged out after our identity provider certificate renewal and SAML "
        "sign-in reports a signature problem.",
    ),
    (
        "KI-003",
        "public-api",
        "List endpoints return 500 when page_size exceeds 500",
        "GET list endpoints answer HTTP 500 instead of clamping page_size above 500.",
        "Request at most 500 items per page.",
        "open",
        "ERROR api.gateway: unhandled ValueError page_size too large",
        "Our integration asks for 1000 items per page and the API replies with a server error.",
    ),
    (
        "KI-004",
        "public-api",
        "Webhook retries stop after three timeouts",
        "When a customer endpoint times out three times the webhook is dropped silently and "
        "never retried.",
        "Re-send the event from the webhook log page.",
        "open",
        "ERROR api.webhook: delivery timeout attempts=3 giving up",
        "Our receiver was briefly slow and now several task events were never redelivered.",
    ),
    (
        "KI-005",
        "permissions",
        "Renaming a role drops its scopes until re-saved",
        "After renaming a custom role members get 403 on projects; saving the role again "
        "restores access.",
        "Open the role and press Save once more after renaming.",
        "fixed",
        "ERROR perm.matrix: unknown role id resolved to empty scope set",
        "Since an admin changed the name of a role everybody with that role sees access denied "
        "messages.",
    ),
    (
        "KI-006",
        "billing",
        "Duplicate VAT line after billing country change",
        "Changing the billing country mid cycle produces an invoice with the tax line twice.",
        "Support can regenerate the invoice; customers are not double charged.",
        "open",
        "WARN billing.tax: duplicate tax line item",
        "Invoice total looks too high because the VAT row appears two times after we updated "
        "the company address.",
    ),
    (
        "KI-007",
        "billing",
        "Checkout timeout may still capture the card payment",
        "Upgrading a plan can hang and time out at the payment step although the charge succeeded.",
        "Check the invoice list before retrying the payment.",
        "open",
        "ERROR billing.gateway: charge timeout after 30000 ms",
        "The upgrade page timed out but the bank shows the amount was taken.",
    ),
    (
        "KI-008",
        "reporting",
        "CSV export applies the timezone twice",
        "Dates in exported CSV reports are shifted by double the workspace timezone offset.",
        "Set the workspace timezone to UTC before exporting.",
        "fixed",
        "WARN reporting.export: tz applied twice",
        "All the dates in the exported spreadsheet are a day late compared with the dashboard.",
    ),
    (
        "KI-009",
        "reporting",
        "Quarterly dashboard times out on very large workspaces",
        "The quarterly summary dashboard shows a timeout for workspaces with over 100k tasks.",
        "Narrow the date range to one month.",
        "wontfix",
        "ERROR reporting.query: statement timeout plan=seqscan",
        "Our big workspace cannot open the quarter overview, it spins and then fails with "
        "a timeout.",
    ),
    (
        "KI-010",
        "sync-engine",
        "Conflict loop after long offline editing",
        "Clients that edited offline for a day or more never finish syncing because the merge "
        "keeps detecting conflicts.",
        "Sign out, clear the local cache and sign in again.",
        "open",
        "ERROR sync.merge: conflict loop detected rounds=50",
        "The progress bar of the sync never completes after my laptop was offline all weekend.",
    ),
    (
        "KI-011",
        "file-storage",
        "Multipart upload completion times out above 500 MB",
        "Uploads larger than 500 MB reach 99 percent and then fail when the completion call "
        "times out.",
        "Split the file or upload through the desktop client.",
        "open",
        "ERROR storage.multipart: complete timeout parts=200",
        "A big video attachment gets stuck at the very end of the upload and then errors.",
    ),
    (
        "KI-012",
        "search",
        "Index lag after bulk import",
        "Tasks created through a bulk import are not searchable for up to 15 minutes.",
        "Wait for the indexer to catch up; no action needed.",
        "wontfix",
        "INFO search.indexer: backlog depth=12000",
        "I imported a CSV of tasks and searching for them returns nothing for a while.",
    ),
    (
        "KI-013",
        "web-ui",
        "Board drag and drop freezes with more than 1000 cards",
        "Dragging a card on a board with over 1000 cards freezes the tab in Safari.",
        "Filter the board to fewer cards before reordering.",
        "open",
        "WARN ui.board: long task 4200 ms during dragover",
        "Moving a card on our huge board hangs the page and the browser asks to wait or quit.",
    ),
    (
        "KI-014",
        "mobile-app",
        "Biometric login fails after an OS update",
        "Face or fingerprint login stops working after a phone OS update until biometrics "
        "are enrolled again in the app.",
        "Disable and re-enable biometric login in app settings.",
        "fixed",
        "ERROR mobile.auth: keystore key invalidated",
        "After updating the phone, the app keeps asking for the password and the fingerprint "
        "option is rejected.",
    ),
    (
        "KI-015",
        "notifications",
        "Digest email duplicated when two schedulers overlap",
        "Users receive the daily digest twice when the scheduler failover overlaps with the "
        "primary.",
        "No action needed; duplicates stop after the failover window.",
        "open",
        "WARN notify.digest: lock not acquired, sending anyway",
        "My team got two identical digest emails this morning.",
    ),
]

USE_CASES: list[tuple[str, str, list[str]]] = [
    (
        "Sign in with company SSO",
        "Employees sign in through the corporate identity provider.",
        ["auth-sso", "permissions"],
    ),
    (
        "Invite external guests",
        "Share one project with guests without exposing the workspace.",
        ["permissions", "auth-sso", "notifications"],
    ),
    (
        "Automate with the public API",
        "Integrations create and read tasks through REST and webhooks.",
        ["public-api", "permissions"],
    ),
    (
        "Upgrade plan and pay invoices",
        "Admins change plans, pay by card and download invoices.",
        ["billing", "notifications"],
    ),
    (
        "Quarterly progress reporting",
        "Managers build dashboards and export reports to CSV.",
        ["reporting", "search"],
    ),
    (
        "Work offline on mobile",
        "Edit tasks on the phone without connectivity and sync later.",
        ["mobile-app", "sync-engine"],
    ),
    (
        "Share files on tasks",
        "Attach, preview and download files on tasks.",
        ["file-storage", "web-ui", "search"],
    ),
    (
        "Plan with board and Gantt views",
        "Visual planning with drag and drop boards and timelines.",
        ["web-ui", "sync-engine"],
    ),
]

# component -> list of (title, description, log) templates with {slots}
Scenario = tuple[str, str, str]
SCENARIOS: dict[str, list[Scenario]] = {
    "auth-sso": [
        (
            "Login redirect loop after SSO sign-in on {browser}",
            "Users in {wsid} sign in through the corporate IdP and are bounced between /login and "
            "/sso/callback until the browser gives up. Clearing cookies helps for one "
            "attempt only.",
            "{ts} WARN auth.sso callback: state cookie missing, restarting login flow attempt={n}",
        ),
        (
            "SAML assertion rejected: audience mismatch",
            "Login via SAML fails with a generic error page. After the IdP metadata was "
            "rotated the "
            "audience value no longer matches what Larkspur expects for {wsid}.",
            "{ts} ERROR auth.saml: audience mismatch expected=larkspur-{wsid} got=larkspur-legacy",
        ),
        (
            "Session expires right after login, timeout on slow sign-in",
            "Session cookie lifetime is {n}00 seconds instead of the configured 8 hours so users "
            "are logged out right after logging in. Seen when the login request is slow.",
            "{ts} ERROR auth.session: ttl clamp applied ttl={n}00s configured=28800s",
        ),
        (
            "Password reset link says token expired immediately",
            "Password reset link opened within a minute reports that the token has expired. Clock "
            "skew between auth nodes suspected.",
            "{ts} WARN auth.reset: token nbf in future skew={n}s",
        ),
        (
            "MFA code accepted but login ends with a timeout",
            "TOTP codes verify fine yet the sign-in spinner ends with a timeout error. The MFA "
            "verification call is slow for {wsid}.",
            "{ts} ERROR auth.mfa: verify timeout after {n}000 ms",
        ),
        (
            "SCIM provisioning creates duplicate users at first login",
            "Users provisioned by SCIM get a second account the first time they sign in through "
            "SSO, because the email casing differs from the provisioned record.",
            "{ts} WARN auth.scim: no match for subject, creating user email_case_mismatch=true",
        ),
    ],
    "public-api": [
        (
            "GET {endpoint} returns 500 for large page_size",
            "Requesting page_size={n}000 on {endpoint} returns HTTP 500 instead of a clamped page. "
            "Smaller sizes work.",
            "{ts} ERROR api.gateway: unhandled ValueError page_size={n}000 route={endpoint}",
        ),
        (
            "Rate limiter returns 429 with wrong Retry-After header",
            "Clients using the API token for {wsid} receive Retry-After: 0 and hammer the endpoint "
            "which causes a timeout cascade.",
            "{ts} WARN api.ratelimit: bucket exhausted key=tok_{n} retry_after=0",
        ),
        (
            "Webhook delivery times out and is never retried",
            "Outgoing webhook to the customer endpoint times out after 5s and the retry queue "
            "silently drops the event. Customer sees missing task.created events.",
            "{ts} ERROR api.webhook: delivery timeout url=https://hooks.example.test/lark "
            "attempt=1 no retry scheduled",
        ),
        (
            "API token returns 401 after rotation",
            "After rotating the API token in settings the old token is rejected as expected but "
            "the new one returns 401 for up to {n} minutes.",
            "{ts} WARN api.auth: token not found in cache key=tok_{n}",
        ),
        (
            "OpenAPI spec lists removed field assignee_email",
            "Public documentation and the generated client expose a field the {endpoint} response "
            "no longer returns, causing client deserialization errors.",
            "{ts} ERROR api.schema: response missing required field assignee_email",
        ),
        (
            "Bulk export through the API times out for big workspaces",
            "POST /v1/exports for {wsid} with over {n}0000 tasks returns 504 after 30 seconds.",
            "{ts} ERROR api.gateway: upstream timeout 30000 ms route=/v1/exports",
        ),
    ],
    "permissions": [
        (
            "Guest can see private projects in {wsid}",
            "A guest invited to a single project can list all projects from the sidebar. Role "
            "inheritance from the workspace seems to leak read access.",
            "{ts} WARN perm.eval: role=guest inherited scope=project:read:* from workspace default",
        ),
        (
            "Access denied everywhere after role rename",
            "Renaming a custom role in admin settings makes members lose access to every project "
            "until the role is saved again. Login works but pages show 403.",
            "{ts} ERROR perm.matrix: unknown role id role_{n} resolved to empty scope set",
        ),
        (
            "Permission check timeout on workspaces with many groups",
            "Opening a project in a workspace with {n}0 nested groups takes 20 seconds and "
            "sometimes times out because membership is resolved recursively.",
            "{ts} WARN perm.groups: resolve depth={n} elapsed_ms={n}000",
        ),
        (
            "Cannot revoke write scope for service accounts",
            "Unticking the write scope on the service-account page saves without error but the "
            "key keeps working for writes.",
            "{ts} INFO perm.scopes: update ignored, scope immutable on service principal",
        ),
        (
            "Export button visible for viewers but returns 403",
            "Viewers see the Export button, click it and get a 403. The permission should hide "
            "the button or allow a summary export.",
            "{ts} ERROR perm.check: deny action=export.create role=viewer",
        ),
        (
            "Group membership change takes an hour to apply",
            "Adding a user to a group in {wsid} does not grant project access until about an hour "
            "later. Permission cache never invalidated.",
            "{ts} INFO perm.cache: ttl=3600 key=group_{n} not invalidated",
        ),
    ],
    "billing": [
        (
            "Invoice shows tax twice for EU customers",
            "VAT is applied twice on invoices generated for {wsid} when the billing address "
            "country changes mid cycle.",
            "{ts} WARN billing.tax: duplicate tax line item invoice=INV-{n}0{n}",
        ),
        (
            "Card payment hangs and times out at checkout",
            "Upgrading the plan hangs and times out at the payment step. The card is sometimes "
            "charged anyway.",
            "{ts} ERROR billing.gateway: charge timeout after 30000 ms idempotency_key=ik_{n}",
        ),
        (
            "Proration wrong when seats are removed mid month",
            "Removing {n} seats on the 15th credits the full month instead of the remaining "
            "half. Invoice preview shows the wrong amount.",
            "{ts} WARN billing.proration: days_remaining=15 used_days=30 seats_removed={n}",
        ),
        (
            "Invoice PDF missing line items",
            "Downloaded invoice PDF omits add-on lines although the on-screen invoice shows them. "
            "The PDF template drops items beyond line 20.",
            "{ts} WARN billing.pdf: truncated line items rendered=20 total={n}0",
        ),
        (
            "Subscription renewal email sent but plan not extended",
            "The renewal confirmation email arrives but the workspace shows the plan as expired "
            "the next morning.",
            "{ts} ERROR billing.renewal: payment captured, subscription update failed sub_{n}",
        ),
        (
            "Coupon code applies the discount twice",
            "Entering a coupon at checkout reduces the price by double the stated percentage "
            "when the plan is annual.",
            "{ts} WARN billing.coupon: applied twice code=SPRING{n}0 cart=cart_{n}",
        ),
    ],
    "reporting": [
        (
            "Burndown CSV export has shifted dates",
            "Exported CSV timestamps are offset by the workspace timezone twice so tasks show up "
            "a day later than on the chart.",
            "{ts} WARN reporting.export: tz applied twice tz=Europe/Berlin",
        ),
        (
            "Quarterly dashboard timeout on large workspaces",
            "The quarterly summary dashboard for {wsid} spins for 60s and then shows a timeout "
            "error. The aggregation query scans the full activity table.",
            "{ts} ERROR reporting.query: statement timeout 60000 ms plan=seqscan activity",
        ),
        (
            "Scheduled report email contains yesterday's numbers",
            "The Monday report email shows figures from Sunday morning. The scheduler runs before "
            "the nightly aggregation finishes.",
            "{ts} INFO reporting.schedule: report_{n} started before rollup complete",
        ),
        (
            "Velocity chart double counts reopened tasks",
            "Tasks that were reopened {n} times are counted once per reopening in the velocity "
            "chart so the sprint total is inflated.",
            "{ts} WARN reporting.velocity: task_{n} counted rows={n}",
        ),
        (
            "Report export fails with 500 when a title contains emoji",
            "Exporting a report to CSV fails with a server error if any task title contains an "
            "emoji. Plain ASCII titles export fine.",
            "{ts} ERROR reporting.export: UnicodeEncodeError cp1252 report_{n}",
        ),
        (
            "Custom report filter on label ignores case",
            "A report filtered by label Backend omits tasks labelled backend. Filters in the "
            "board view are case insensitive.",
            "{ts} INFO reporting.filter: label eq 'Backend' matched={n}",
        ),
    ],
    "sync-engine": [
        (
            "Sync stuck at {n}0% after offline edits",
            "Devices that edited tasks offline for a day never finish syncing. The progress bar "
            "stalls and the sync queue shows a conflict loop.",
            "{ts} ERROR sync.merge: conflict loop detected doc=task_{n} rounds=50",
        ),
        (
            "Duplicate tasks created after sync on reconnect",
            "After reconnecting the client uploads queued creates twice, so each task created "
            "offline appears two times.",
            "{ts} WARN sync.queue: replayed op ids already applied count={n}",
        ),
        (
            "Initial sync timeout for workspaces with many attachments",
            "First sync for {wsid} times out after 120 s because attachment metadata is fetched "
            "one item at a time.",
            "{ts} ERROR sync.initial: timeout after 120000 ms fetched={n}00 of {n}000",
        ),
        (
            "Deleted comments reappear after sync",
            "Comments deleted on the web come back on a second device after sync. Tombstones are "
            "garbage collected too early.",
            "{ts} WARN sync.gc: tombstone for comment_{n} removed before replica ack",
        ),
        (
            "Several minutes of lag between web and desktop clients",
            "Edits show up on the other client after {n} minutes. Replication lag grows when many "
            "members edit one project.",
            "{ts} INFO sync.replica: lag_ms={n}0000 shard=s{n}",
        ),
        (
            "Forced sign-in again when the sync cursor expires",
            "Clients are asked to log in again when the sync cursor expires because the refresh "
            "call returns 410.",
            "{ts} ERROR sync.cursor: refresh failed status=410 cursor_age_h={n}0",
        ),
    ],
    "file-storage": [
        (
            "Upload fails at 99% for files over {n}00 MB",
            "Large attachment uploads reach 99% and then fail. The multipart completion call "
            "times out.",
            "{ts} ERROR storage.multipart: complete timeout upload_id=up_{n} parts=200",
        ),
        (
            "Project archive export produces a corrupt zip",
            "Project archive export (zip) cannot be opened, the central directory is missing. "
            "Happens with more than {n}00 files.",
            "{ts} ERROR storage.archive: stream closed before central directory files={n}00",
        ),
        (
            "Thumbnails not generated for HEIC images",
            "Photos uploaded from phones show a grey placeholder. The thumbnail worker skips HEIC "
            "files.",
            "{ts} WARN storage.thumb: unsupported mime image/heic file_{n}",
        ),
        (
            "Download link expires before the stated 24 hours",
            "Signed download links stop working after {n} hours instead of 24. Users get an "
            "access error from the storage host.",
            "{ts} WARN storage.sign: ttl={n}h requested=24h",
        ),
        (
            "Storage quota shows 0 bytes after cleanup",
            "After deleting old attachments the quota page reports 0 bytes used, then jumps back "
            "after a few hours.",
            "{ts} INFO storage.quota: recompute pending {wsid} used_bytes=0",
        ),
        (
            "Virus scan timeout blocks attachment upload",
            "Uploads of PDF attachments hang on 'scanning' and time out after 60 s when the scan "
            "queue is busy.",
            "{ts} ERROR storage.scan: timeout after 60000 ms queue_depth={n}00",
        ),
    ],
    "search": [
        (
            "Search misses tasks created in the last hour",
            "Searching for a task title created {n}0 minutes ago returns nothing. The indexer "
            "worker is behind.",
            "{ts} WARN search.indexer: lag_seconds={n}000 shard=s{n}",
        ),
        (
            "Search timeout when the query contains a wildcard",
            "Queries such as *report* take over 30 seconds and end with a timeout in {wsid}.",
            "{ts} ERROR search.query: timeout 30000 ms wildcard=leading",
        ),
        (
            "Autocomplete suggests archived projects",
            "Typing in the quick switcher offers projects archived long ago and ranks them above "
            "active ones.",
            "{ts} INFO search.suggest: filter archived=false not applied",
        ),
        (
            "Quoted phrase search ignores word order",
            'Searching for "release notes draft" also returns tasks with the words in another '
            "order. Phrase matching seems disabled.",
            "{ts} WARN search.query: phrase slop={n} (expected 0)",
        ),
        (
            "Search index rebuild loops for {wsid}",
            "A reindex of the workspace restarts every {n} minutes and never finishes, so results "
            "stay stale.",
            "{ts} ERROR search.reindex: restarted batch={n} reason=version_conflict",
        ),
        (
            "Search returns 500 for non-latin queries",
            "Searching with Cyrillic or Japanese text returns an error page. English queries work.",
            "{ts} ERROR search.query: analyzer missing for lang=ja query_{n}",
        ),
    ],
    "web-ui": [
        (
            "Board drag and drop freezes in {browser}",
            "Dragging a card to another column freezes the tab for several seconds in {browser}. "
            "CPU spikes to 100%.",
            "{ts} WARN ui.board: long task {n}000 ms during dragover",
        ),
        (
            "Dark mode makes the comment editor unreadable",
            "In dark mode the comment editor shows dark grey text on a black background. Light "
            "mode is fine.",
            "{ts} INFO ui.theme: css var --editor-fg unresolved theme=dark",
        ),
        (
            "Login page layout broken on narrow windows",
            "The login form overflows below 400 px width and the submit button is out of reach "
            "in {browser}.",
            "{ts} INFO ui.layout: viewport={n}00 overflow-x detected .login-card",
        ),
        (
            "Gantt view freezes with 500+ tasks",
            "Opening the Gantt view for a project with {n}00 tasks freezes the page and "
            "{browser} reports a script timeout.",
            "{ts} ERROR ui.gantt: script timeout render tasks={n}00",
        ),
        (
            "Export dialog closes without starting a download in {browser}",
            "Clicking Export in the toolbar closes the dialog and no file is downloaded. A popup "
            "blocker is suspected.",
            "{ts} WARN ui.export: window.open returned null",
        ),
        (
            "Keyboard shortcut for new task conflicts with browser find",
            "Pressing the shortcut for a new task opens the browser find bar in {browser} instead.",
            "{ts} INFO ui.shortcuts: preventDefault skipped key=ctrl+f",
        ),
    ],
    "mobile-app": [
        (
            "App crashes on launch after update on {mobile}",
            "Since the latest app version the app closes immediately after the splash screen on "
            "{mobile}.",
            "{ts} FATAL mobile.boot: NullPointerException in SplashActivity device={mobile}",
        ),
        (
            "Login with biometrics fails after OS update on {mobile}",
            "Face or fingerprint sign-in is rejected after a phone update to {mobile}. The "
            "password login still works.",
            "{ts} ERROR mobile.auth: keystore key invalidated device={mobile}",
        ),
        (
            "Offline mode shows stale tasks until pull to refresh",
            "After a day without connection the task list shows old data until the user pulls to "
            "refresh on {mobile}.",
            "{ts} INFO mobile.cache: serving cached list age_h={n}0",
        ),
        (
            "Photo upload from camera roll fails on {mobile}",
            "Attaching a photo to a task fails with 'upload error' on {mobile}. Small screenshots "
            "work, camera photos fail.",
            "{ts} ERROR mobile.upload: request entity too large size={n}0MB",
        ),
        (
            "Deep link from email opens the wrong project",
            "Tapping a task link in the notification email opens the last project instead of the "
            "linked task on {mobile}.",
            "{ts} WARN mobile.link: route param task_{n} dropped by router",
        ),
        (
            "Battery drain from background sync on {mobile}",
            "The app uses {n}0% of battery per day on {mobile} even when idle. Background "
            "refresh runs every minute.",
            "{ts} INFO mobile.bg: wakeups per hour={n}0",
        ),
    ],
    "notifications": [
        (
            "Daily digest email sent twice for {wsid}",
            "All members of {wsid} received the daily digest email twice this morning.",
            "{ts} WARN notify.digest: lock not acquired, sending anyway batch={n}",
        ),
        (
            "Push notification delayed by {n}0 minutes",
            "Mentions arrive as push notifications {n}0 minutes late. Email arrives instantly.",
            "{ts} INFO notify.push: queue wait ms={n}00000 provider=primary",
        ),
        (
            "Mentions of SCIM provisioned users never notify",
            "Users created by SCIM provisioning never get a notification when mentioned. Manually "
            "invited users do.",
            "{ts} WARN notify.mention: no channel for user_{n} (preferences missing)",
        ),
        (
            "Unsubscribe link in the digest returns 404",
            "Clicking unsubscribe at the bottom of the notification email shows a 404 page.",
            "{ts} INFO notify.unsub: token not found token_{n}",
        ),
        (
            "Webhook-based chat alert times out",
            "Notifications routed to the team chat integration time out after 10 s and the alert "
            "is lost.",
            "{ts} ERROR notify.chat: delivery timeout 10000 ms integration_{n}",
        ),
        (
            "Quiet hours ignored for push notifications",
            "Push notifications still arrive at night although quiet hours are configured on "
            "{mobile}.",
            "{ts} INFO notify.push: quiet_hours not evaluated tz=unset",
        ),
    ],
}

# Deliberately misleading cases: (title, description, log, true component)
AMBIGUOUS: list[tuple[str, str, str, str]] = [
    (
        "Export to CSV button greyed out in the web UI",
        "The toolbar button is disabled when a file over 2 GB is attached. The UI is behaving "
        "correctly: the storage service rejects the manifest write with a 413, so the export "
        "never becomes available.",
        "2026-04-02T09:12:44Z ERROR storage.manifest: 413 payload too large manifest_write",
        "file-storage",
    ),
    (
        "Timeout when opening the dashboard in the mobile app",
        "The phone only shows a spinner. The cause is on the server: the quarterly invoice "
        "summary query runs for 40 seconds and the app request times out. Same report is slow "
        "in the browser.",
        "2026-04-03T11:30:02Z ERROR reporting.query: statement timeout 40000 ms",
        "reporting",
    ),
    (
        "Login succeeds but every project page says Access denied",
        "Sign-in and SSO work. After login, guest users land on 403 pages because the guest role "
        "lacks the project:read scope in the role matrix.",
        "2026-04-04T08:01:19Z ERROR perm.check: deny action=project.read role=guest",
        "permissions",
    ),
    (
        "Notification emails stop after invoice paid",
        "Billing marks the invoice as paid and emits the event correctly. The email worker drops "
        "the event because the recipient locale is null, so no receipt email goes out.",
        "2026-04-05T13:44:51Z WARN notify.render: locale is None, dropping event invoice.paid",
        "notifications",
    ),
    (
        "Search results missing files that were just uploaded",
        "The uploads succeed and the files are visible in storage. They are missing from search "
        "because the indexer skips documents whose mime type was recorded as "
        "application/octet-stream.",
        "2026-04-06T10:20:33Z WARN search.indexer: skipped mime=application/octet-stream",
        "search",
    ),
    (
        "Mobile sync stuck at 99% after login",
        "The phone looks frozen on the sync screen after sign-in. On the server the merge keeps "
        "re-applying a tombstone for a deleted checklist and never converges, which would also "
        "happen on a desktop client.",
        "2026-04-07T07:55:12Z ERROR sync.merge: tombstone reapplied doc=checklist rounds=50",
        "sync-engine",
    ),
    (
        "Timeout calling the tasks endpoint from the web UI",
        "The browser shows a request timeout, but the app is fine. The API gateway returns 429 "
        "with Retry-After set to zero and the client keeps retrying until it gives up.",
        "2026-04-08T15:03:27Z WARN api.ratelimit: bucket exhausted retry_after=0",
        "public-api",
    ),
    (
        "Report export shows the wrong currency symbol in the UI",
        "The exported file is correct. The page header renders the euro sign for USD workspaces "
        "because the front-end formats numbers with the browser locale instead of the workspace "
        "currency.",
        "2026-04-09T12:41:08Z INFO ui.format: Intl locale=de-DE currency override missing",
        "web-ui",
    ),
    (
        "Push notification opens the login screen",
        "Tapping a push notification shows the sign-in screen even though the user is logged "
        "in. The deep link handler in the app loses the session token when it cold-starts.",
        "2026-04-10T18:09:46Z WARN mobile.link: session token not restored on cold start",
        "mobile-app",
    ),
    (
        "Billing page crashes with a permission error",
        "Workspace admins get 403 on the billing page since the role rename. The billing service "
        "is healthy, the billing_admin role is missing from the permission matrix.",
        "2026-04-11T09:33:15Z ERROR perm.matrix: role billing_admin not found",
        "permissions",
    ),
]

SLOTS: dict[str, Callable[[random.Random], str]] = {
    "browser": lambda r: r.choice(["Chrome 126", "Firefox 128", "Safari 17", "Edge 126"]),
    "mobile": lambda r: r.choice(["iOS 17.5", "iOS 18.1", "Android 13", "Android 14"]),
    "wsid": lambda r: f"ws-{r.randint(1000, 9999)}",
    "n": lambda r: str(r.randint(2, 9)),
    "endpoint": lambda r: r.choice(["/v1/tasks", "/v1/projects", "/v1/comments", "/v1/members"]),
    "ts": lambda r: (
        f"2026-0{r.randint(1, 4)}-{r.randint(10, 28)}"
        f"T{r.randint(0, 23):02d}:{r.randint(0, 59):02d}:{r.randint(0, 59):02d}Z"
    ),
}

SUFFIXES = [
    " Several users are affected.",
    " Started this week.",
    " Customer is asking for an update.",
    " Seen again today.",
]
SEVERITIES = ["low", "medium", "high", "critical"]
SEV_WEIGHTS = [25, 40, 25, 10]
CONTEXT = [
    " Reported by support for {wsid}.",
    " Happens on {browser}.",
    " Reproduced twice on staging.",
    " No recent deploy that we know of.",
]


def _fill(templates: list[str], rng: random.Random) -> list[str]:
    values: dict[str, str] = {}
    out: list[str] = []
    for tpl in templates:
        for _, field, _, _ in string.Formatter().parse(tpl):
            if field and field not in values:
                values[field] = SLOTS[field](rng)
        out.append(tpl.format(**values))
    return out


def _assignee(rng: random.Random, component: str) -> str:
    team = next(t for t, v in TEAMS.items() if component in v["components"])
    default = COMPONENTS[component]["assignee"]
    if rng.random() < 0.6:
        return str(default)
    return str(rng.choice(TEAMS[team]["members"]))


def _team_of(component: str) -> str:
    return next(t for t, v in TEAMS.items() if component in v["components"])


def _record(
    rng: random.Random,
    bug_id: str,
    title: str,
    desc: str,
    logs: str,
    component: str,
    duplicate_of: str | None = None,
    known_issue: str | None = None,
    assignee: str | None = None,
    severity: str | None = None,
) -> dict[str, Any]:
    return {
        "id": bug_id,
        "title": title,
        "description": desc,
        "logs": logs,
        "component": component,
        "team": _team_of(component),
        "assignee": assignee or _assignee(rng, component),
        "severity": severity or rng.choices(SEVERITIES, SEV_WEIGHTS)[0],
        "duplicate_of": duplicate_of,
        "known_issue": known_issue,
    }


def _scenario_bug(rng: random.Random, bug_id: str, component: str) -> dict[str, Any]:
    title, desc, log = _fill(list(rng.choice(SCENARIOS[component])), rng)
    if rng.random() < 0.4:
        desc += _fill([rng.choice(CONTEXT)], rng)[0]
    return _record(rng, bug_id, title, desc, log, component)


def _ki_bug(rng: random.Random, bug_id: str, ki: tuple[str, ...], alt: bool) -> dict[str, Any]:
    ki_id, component, title, symptoms, _wk, _st, log, alt_text = ki
    desc = alt_text if alt else symptoms
    ctx = _fill([rng.choice(CONTEXT)], rng)[0]
    prefix = rng.choice(["", "Customer report: ", "Again: "])
    ts = _fill(["{ts}"], rng)[0]
    return _record(
        rng, bug_id, prefix + title, desc + ctx, f"{ts} {log}", component, known_issue=ki_id
    )


def _dup_of(rng: random.Random, bug_id: str, orig: dict[str, Any]) -> dict[str, Any]:
    dup = dict(orig)
    dup["id"] = bug_id
    dup["description"] = orig["description"] + rng.choice(SUFFIXES)
    dup["severity"] = orig["severity"]
    dup["duplicate_of"] = orig["id"]
    return dup


def build_history(rng: random.Random, n: int = 150) -> list[dict[str, Any]]:
    """History with ~15% duplicates and ~20% known-issue bugs."""
    out: list[dict[str, Any]] = []
    comps = list(COMPONENTS)
    for i in range(n):
        bug_id = f"BUG-{1001 + i}"
        roll = rng.random()
        originals = [b for b in out if b["duplicate_of"] is None]
        if roll < 0.15 and len(originals) >= 5:
            out.append(_dup_of(rng, bug_id, rng.choice(originals)))
        elif roll < 0.31:
            out.append(_ki_bug(rng, bug_id, rng.choice(KNOWN_ISSUES), alt=False))
        else:
            out.append(_scenario_bug(rng, bug_id, rng.choice(comps)))
    return out


def build_eval(rng: random.Random, history: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """40 held-out bugs: 6 duplicates, 8 known-issue hits, 10 ambiguous, 16 plain."""
    items: list[dict[str, Any]] = []
    originals = [b for b in history if b["duplicate_of"] is None]
    for orig in rng.sample(originals, 6):
        items.append(_dup_of(rng, "", orig))
    for ki in rng.sample(KNOWN_ISSUES, 8):
        items.append(_ki_bug(rng, "", ki, alt=True))
    for title, desc, log, comp in AMBIGUOUS:
        items.append(_record(rng, "", title, desc, log, comp))
    comps = list(COMPONENTS)
    for _ in range(16):
        items.append(_scenario_bug(rng, "", rng.choice(comps)))
    rng.shuffle(items)
    for i, item in enumerate(items, start=1):
        item["id"] = f"EVAL-{i:03d}"
    return items


def _write_yaml(path: Path, key: str, items: list[dict[str, Any]]) -> None:
    path.write_text(
        yaml.safe_dump({key: items}, sort_keys=False, allow_unicode=True, width=100),
        encoding="utf-8",
    )


def _write_jsonl(path: Path, items: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(i, ensure_ascii=False) + "\n" for i in items), encoding="utf-8"
    )


def generate(out_dir: Path) -> None:
    """Write all data files into out_dir (deterministic)."""
    out_dir.mkdir(parents=True, exist_ok=True)
    teams = [{"name": n, **v} for n, v in TEAMS.items()]
    components = [
        {
            "name": name,
            "owner_team": _team_of(name),
            "default_assignee": spec["assignee"],
            "keywords": spec["keywords"],
        }
        for name, spec in COMPONENTS.items()
    ]
    known_issues = [
        {
            "id": k[0],
            "title": k[2],
            "component": k[1],
            "symptoms": k[3],
            "workaround": k[4],
            "status": k[5],
        }
        for k in KNOWN_ISSUES
    ]
    use_cases = [{"name": n, "description": d, "components": c} for n, d, c in USE_CASES]
    history = build_history(random.Random(42))
    eval_set = build_eval(random.Random(7), history)
    _write_yaml(out_dir / "teams.yaml", "teams", teams)
    _write_yaml(out_dir / "components.yaml", "components", components)
    _write_yaml(out_dir / "known_issues.yaml", "known_issues", known_issues)
    _write_yaml(out_dir / "use_cases.yaml", "use_cases", use_cases)
    _write_jsonl(out_dir / "history.jsonl", history)
    _write_jsonl(out_dir / "eval.jsonl", eval_set)


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate the invented Larkspur data set.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output directory")
    args = parser.parse_args(argv)
    generate(args.out)
    sys.stdout.write(f"wrote data set to {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
