#!/usr/bin/env python3
"""Create the demo git repo: a TS/Express billing service with a bad PR branch.

  main             base service + the ai-review kit installed
  feature/invoices invoices API, reminders job, migration, hardcoded key, …

Usage: setup_demo_repo.py <target-dir>   (target must not exist or be empty)
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SERVICE = HERE / "sample_service"
DEMO_CONFIG = {"gate": "blocker", "max_findings": 25}
# Assembled at runtime so this repo never contains a literal key-shaped string
# (secret scanners on *this* repo would rightly block it).
FAKE_KEY = "sk_" + "live_" + "51NxDemoKeyAbCdEfGhIjKlMnOpQr"


def git(repo: Path, *args: str) -> None:
    # Bypass global hooks: the demo PR deliberately contains a (fake) secret.
    subprocess.run(
        ["git", "-c", "core.hooksPath=/dev/null", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )


def copy_tree(src: Path, dst: Path) -> None:
    for f in src.rglob("*"):
        if f.is_file():
            out = dst / f.relative_to(src)
            out.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f, out)


def setup(target: Path) -> Path:
    sys.path.insert(0, str(HERE.parent / "src"))
    from aireview.install import install

    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"{target} exists and is not empty")
    target.mkdir(parents=True, exist_ok=True)

    git(target, "init", "-q", "-b", "main")
    git(target, "config", "user.email", "demo@example.com")
    git(target, "config", "user.name", "Demo Dev")
    git(target, "config", "commit.gpgsign", "false")

    copy_tree(SERVICE / "base", target)
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "billing-service v1.4.0")

    install(target)
    cfg_path = target / ".ai-review" / "config.json"
    cfg = json.loads(cfg_path.read_text())
    cfg.update(DEMO_CONFIG, base="main")
    cfg_path.write_text(json.dumps(cfg, indent=2) + "\n")
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "Add AI review kit (.ai-review, adapters, CI)")

    git(target, "checkout", "-q", "-b", "feature/invoices")
    copy_tree(SERVICE / "pr", target)
    cfg_ts = target / "src" / "config.ts"
    cfg_ts.write_text(cfg_ts.read_text().replace("__DEMO_STRIPE_KEY__", FAKE_KEY))
    git(target, "add", "-A")
    git(target, "commit", "-q", "-m", "Invoices API + overdue reminders")

    out = target / ".ai-review" / "out"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "pr_body.md", out / "pr_body.md")
    return target


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(setup(Path(sys.argv[1]).resolve()))
