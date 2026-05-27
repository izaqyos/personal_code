from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from playwright.async_api import async_playwright

_log = logging.getLogger("gam")


class AuthStatus(Enum):
    MISSING = "missing"
    INVALID = "invalid"
    PRESENT = "present"


@dataclass(frozen=True)
class AuthStatusResult:
    status: AuthStatus
    message: str


def save_storage_state(payload: dict, target: Path) -> None:
    """Write storage_state.json with parents and 0600 perms."""
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp = target.with_suffix(target.suffix + ".tmp")
    tmp.write_text(json.dumps(payload))
    os.chmod(tmp, 0o600)
    os.replace(tmp, target)


def check_storage_state(path: Path) -> AuthStatusResult:
    """Cheap local check — does the file exist and parse as JSON?

    Does NOT contact GitHub. For an online check use `verify_storage_state_live`
    (added when the `auth status` subcommand is wired up — see CLI task).
    """
    if not path.exists():
        return AuthStatusResult(AuthStatus.MISSING, f"no file at {path}")
    try:
        json.loads(path.read_text())
    except (json.JSONDecodeError, OSError) as e:
        return AuthStatusResult(AuthStatus.INVALID, f"could not parse: {e}")
    return AuthStatusResult(AuthStatus.PRESENT, f"present at {path}")


async def interactive_login(storage_state_path: Path) -> None:
    """Open a headed chromium window pointed at github.com/login.

    Wait for the user to finish signing in (SSO/2FA/whatever) by polling for the
    presence of the meta[name=user-login] tag on a github.com page that isn't
    /login. Save the resulting BrowserContext.storage_state() to disk.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        try:
            ctx = await browser.new_context()
            page = await ctx.new_page()
            print(
                "\nA browser window will open. Sign in to GitHub (incl. SSO/2FA), "
                "then this command will detect the session and save it.\n"
            )
            await page.goto("https://github.com/login")
            # Wait for any github.com page that isn't /login and has a user-login meta.
            await page.wait_for_function(
                """() => {
                    const meta = document.querySelector('meta[name="user-login"]');
                    return meta && meta.getAttribute('content') &&
                        !location.pathname.startsWith('/login') &&
                        location.host === 'github.com';
                }""",
                timeout=300_000,  # 5 min for SSO/2FA
            )
            state = await ctx.storage_state()
            login = await page.evaluate(
                "() => document.querySelector('meta[name=\"user-login\"]').content"
            )
            save_storage_state(state, storage_state_path)
            print(f"Logged in as {login}. Session saved to {storage_state_path} (mode 600).")
        finally:
            await browser.close()
