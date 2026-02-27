#!/usr/bin/env python3
"""
Backup Specialist Agent CLI

Unified interface for monitoring and managing the backup system:
- Git backup (dotfiles, obsidian, repos -> GitHub)
- OneDrive backup (archives -> cloud)
- Obsidian checkpoint (local snapshots)
"""

import argparse
import os
import plistlib
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────

HOME = Path.home()
GIT_BACKUP_DIR = HOME / "work/git/git_backup"
LAUNCH_AGENTS_DIR = HOME / "Library/LaunchAgents"
ONEDRIVE_PATH = HOME / "Library/CloudStorage/OneDrive-CheckPointSoftwareTechnologiesLtd"
ONEDRIVE_BACKUP_DIR = ONEDRIVE_PATH / "Backups"
CHECKPOINT_BACKUP_DIR = HOME / "work/backup/obsidian"
VENV_PYTHON = GIT_BACKUP_DIR / "yosi_general_venv/bin/python"
CONFIG_PATH = GIT_BACKUP_DIR / "config.yaml"
LOG_DIR = GIT_BACKUP_DIR / "logs"

PLIST_JOBS = {
    "gitbackup": {
        "label": "com.yosii.gitbackup",
        "plist": LAUNCH_AGENTS_DIR / "com.yosii.gitbackup.plist",
        "script": GIT_BACKUP_DIR / "backup.py",
        "schedule": "Sun, Tue, Thu @ 15:30",
        "stdout_log": LOG_DIR / "backup_stdout.log",
        "stderr_log": LOG_DIR / "backup_stderr.log",
    },
    "onedrive": {
        "label": "com.yosii.onedrive.backup",
        "plist": LAUNCH_AGENTS_DIR / "com.yosii.onedrive.backup.plist",
        "script": GIT_BACKUP_DIR / "backup_to_onedrive.py",
        "schedule": "Sun @ 16:00",
        "stdout_log": LOG_DIR / "onedrive_stdout.log",
        "stderr_log": LOG_DIR / "onedrive_stderr.log",
    },
    "checkpoint": {
        "label": "com.yosii.obsidian.checkpoint",
        "plist": LAUNCH_AGENTS_DIR / "com.yosii.obsidian.checkpoint.plist",
        "script": GIT_BACKUP_DIR / "backup_obsidian_checkpoint.py",
        "schedule": "Sun @ 15:00",
        "stdout_log": LOG_DIR / "checkpoint_stdout.log",
        "stderr_log": LOG_DIR / "checkpoint_stderr.log",
    },
}

WEEKDAY_NAMES = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]  # config uses Sunday=0 (cron/launchd convention)

# ── Helpers ──────────────────────────────────────────────────────────────────


def _ok(msg):
    print(f"  [OK] {msg}")


def _warn(msg):
    print(f"  [!]  {msg}")


def _crit(msg):
    print(f"  [!!] {msg}")


def _header(title):
    print(f"\n{title}")
    print("  " + "-" * (len(title) - 2))


def _load_config():
    try:
        import yaml
    except ImportError:
        print("Warning: PyYAML not installed, cannot read config.yaml")
        return None
    if not CONFIG_PATH.exists():
        return None
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)


def _last_modified(path: Path) -> str:
    if not path.exists():
        return "never"
    mtime = datetime.fromtimestamp(path.stat().st_mtime)
    return mtime.strftime("%Y-%m-%d %H:%M")


def _age_days(path: Path) -> float:
    if not path.exists():
        return float("inf")
    return (datetime.now() - datetime.fromtimestamp(path.stat().st_mtime)).total_seconds() / 86400


def _format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


# ── Status ───────────────────────────────────────────────────────────────────


def _launchctl_loaded_jobs():
    """Return set of loaded launchctl job labels."""
    try:
        result = subprocess.run(
            ["launchctl", "list"], capture_output=True, text=True, check=False
        )
        return {line.split()[-1] for line in result.stdout.splitlines() if line.strip()}
    except Exception:
        return set()


def _check_launchagents():
    _header("LaunchAgents:")
    loaded = _launchctl_loaded_jobs()
    for key, job in PLIST_JOBS.items():
        label = job["label"]
        is_loaded = label in loaded
        last_log = _last_modified(job["stdout_log"])
        sched = job["schedule"]
        status_str = "Loaded" if is_loaded else "NOT LOADED"
        line = f"{label:<40} {status_str} | Last log: {last_log} | Schedule: {sched}"
        if is_loaded:
            _ok(line)
        else:
            _crit(line)


def _check_git_repos():
    _header("Git Repos:")
    config = _load_config()
    if not config:
        _warn("Could not load config.yaml")
        return

    repos = config.get("repos", {})
    for name, repo_conf in repos.items():
        repo_path = Path(repo_conf.get("local_path", ""))
        if not repo_path.exists():
            _crit(f"{name:<20} Path not found: {repo_path}")
            continue
        try:
            result = subprocess.run(
                ["git", "-C", str(repo_path), "status", "--porcelain"],
                capture_output=True, text=True, check=False,
            )
            changes = len([l for l in result.stdout.strip().splitlines() if l.strip()])
            auto = "[AUTO]" if repo_conf.get("auto_sync") else "[MANUAL]"
            if changes == 0:
                _ok(f"{name:<20} {auto} Clean")
            else:
                _warn(f"{name:<20} {auto} {changes} uncommitted change(s)")
        except Exception as e:
            _crit(f"{name:<20} Error checking status: {e}")


def _check_onedrive():
    _header("OneDrive Backups:")
    if not ONEDRIVE_PATH.exists():
        _crit("OneDrive folder not found — is OneDrive running?")
        return
    if not ONEDRIVE_BACKUP_DIR.exists():
        _warn("Backup folder not found in OneDrive")
        return

    archives = list(ONEDRIVE_BACKUP_DIR.glob("*.tar.gz"))
    if not archives:
        _warn("No backup archives found")
        return

    total_size = sum(a.stat().st_size for a in archives)
    newest = max(archives, key=lambda a: a.stat().st_mtime)
    newest_age = _age_days(newest)
    newest_date = _last_modified(newest)

    line = f"{len(archives)} archives, {_format_size(total_size)} total, newest: {newest_date}"
    if newest_age > 10:
        _crit(f"{line} (stale — {newest_age:.0f} days old)")
    elif newest_age > 7:
        _warn(f"{line} ({newest_age:.0f} days old)")
    else:
        _ok(line)


def _check_checkpoints():
    _header("Local Checkpoints:")
    if not CHECKPOINT_BACKUP_DIR.exists():
        _warn(f"Checkpoint backup dir not found: {CHECKPOINT_BACKUP_DIR}")
        return

    backups = sorted(
        [d for d in CHECKPOINT_BACKUP_DIR.iterdir() if d.is_dir() and d.name.startswith("backup-")],
        key=lambda d: d.stat().st_mtime, reverse=True,
    )
    if not backups:
        _warn("No checkpoint backups found")
        return

    newest = backups[0]
    newest_age = _age_days(newest)
    newest_date = _last_modified(newest)
    line = f"{len(backups)} backup(s), newest: {newest_date}"
    if newest_age > 10:
        _crit(f"{line} (stale — {newest_age:.0f} days old)")
    elif newest_age > 7:
        _warn(f"{line} ({newest_age:.0f} days old)")
    else:
        _ok(line)


def cmd_status(_args):
    print("\n=== Backup System Status ===")
    _check_launchagents()
    _check_git_repos()
    _check_onedrive()
    _check_checkpoints()
    print()


# ── Run ──────────────────────────────────────────────────────────────────────


def _run_script(script_path: Path, dry_run: bool = False):
    if not script_path.exists():
        print(f"Error: script not found: {script_path}")
        return False
    if not VENV_PYTHON.exists():
        print(f"Error: venv python not found: {VENV_PYTHON}")
        return False

    cmd = [str(VENV_PYTHON), str(script_path)]
    if dry_run:
        cmd.append("--dry-run")

    print(f"Running: {' '.join(cmd)}")
    print("-" * 60)
    result = subprocess.run(cmd, cwd=str(GIT_BACKUP_DIR), check=False)
    print("-" * 60)
    if result.returncode == 0:
        print("Completed successfully.")
    else:
        print(f"Exited with code {result.returncode}.")
    return result.returncode == 0


def cmd_run(args):
    target = args.target
    dry_run = args.dry_run

    targets = {
        "git": PLIST_JOBS["gitbackup"]["script"],
        "onedrive": PLIST_JOBS["onedrive"]["script"],
        "checkpoint": PLIST_JOBS["checkpoint"]["script"],
    }

    if target == "all":
        for name, script in targets.items():
            print(f"\n{'='*60}")
            print(f"  Running: {name}")
            print(f"{'='*60}")
            _run_script(script, dry_run)
    else:
        if target not in targets:
            print(f"Unknown target: {target}. Choose from: git, onedrive, checkpoint, all")
            sys.exit(1)
        _run_script(targets[target], dry_run)


# ── Config ───────────────────────────────────────────────────────────────────


def cmd_config(args):
    action = args.action

    if action == "show":
        config = _load_config()
        if not config:
            print("Could not load config.")
            sys.exit(1)
        print(f"\nConfig: {CONFIG_PATH}\n")
        repos = config.get("repos", {})
        print(f"Repositories ({len(repos)}):")
        for name, rc in repos.items():
            sync = "auto-sync" if rc.get("auto_sync") else "monitor"
            print(f"  {name:<20} [{sync}]  {rc.get('local_path', '?')}")

        sched = config.get("schedule", {})
        print(f"\nSchedule:")
        main = sched.get("main_backup", {})
        days = [WEEKDAY_NAMES[d] for d in main.get("weekdays", [])]
        print(f"  Main backup: {', '.join(days)} @ {main.get('hour', '?')}:{main.get('minute', 0):02d}")
        cp = sched.get("checkpoint_backup", {})
        print(f"  Checkpoint:  {WEEKDAY_NAMES[cp.get('weekday', 0)]} @ {cp.get('hour', '?')}:{cp.get('minute', 0):02d}")

        log_conf = config.get("logging", {})
        print(f"\nLogging:")
        print(f"  File: {log_conf.get('log_file', 'N/A')}")
        print(f"  Level: {log_conf.get('level', 'N/A')}")

        notif = config.get("notifications", {}).get("email", {})
        print(f"\nNotifications:")
        print(f"  Email: {'enabled' if notif.get('enabled') else 'disabled'} -> {notif.get('to', 'N/A')}")
        print()

    elif action == "edit":
        editor = os.environ.get("EDITOR", "vim")
        os.execvp(editor, [editor, str(CONFIG_PATH)])

    elif action == "validate":
        print("\nValidating backup configuration...\n")
        config = _load_config()
        if not config:
            _crit("Cannot load config.yaml")
            sys.exit(1)
        errors = 0
        repos = config.get("repos", {})
        for name, rc in repos.items():
            lp = Path(rc.get("local_path", ""))
            if lp.exists():
                _ok(f"{name}: path exists ({lp})")
            else:
                _crit(f"{name}: path NOT found ({lp})")
                errors += 1
        obs = config.get("repos", {}).get("obsidian_notes", {})
        src = Path(obs.get("source_dir", ""))
        if src.exists():
            _ok(f"Obsidian source: {src}")
        else:
            _crit(f"Obsidian source NOT found: {src}")
            errors += 1
        cp = config.get("checkpoint_backup", {})
        cp_src = Path(cp.get("source", ""))
        cp_dst = Path(cp.get("destination", ""))
        for label, p in [("Checkpoint source", cp_src), ("Checkpoint dest", cp_dst)]:
            if p.exists():
                _ok(f"{label}: {p}")
            else:
                _warn(f"{label} NOT found: {p}")
                errors += 1
        if VENV_PYTHON.exists():
            _ok(f"Venv python: {VENV_PYTHON}")
        else:
            _crit(f"Venv python NOT found: {VENV_PYTHON}")
            errors += 1
        for key, job in PLIST_JOBS.items():
            if job["plist"].exists():
                _ok(f"Plist {key}: {job['plist']}")
            else:
                _crit(f"Plist {key} NOT found: {job['plist']}")
                errors += 1
        print(f"\nValidation complete: {errors} issue(s) found.\n")

    else:
        print(f"Unknown config action: {action}")
        sys.exit(1)


# ── Launchctl ────────────────────────────────────────────────────────────────


def _resolve_job(name: str) -> dict:
    if name in PLIST_JOBS:
        return PLIST_JOBS[name]
    for key, job in PLIST_JOBS.items():
        if name in job["label"]:
            return job
    print(f"Unknown job: {name}. Options: {', '.join(PLIST_JOBS.keys())}")
    sys.exit(1)


def cmd_launchctl(args):
    action = args.action

    if action == "status":
        loaded = _launchctl_loaded_jobs()
        print("\nLaunchAgent Status:")
        print(f"  {'Label':<40} {'Status':<14} {'Schedule'}")
        print("  " + "-" * 80)
        for key, job in PLIST_JOBS.items():
            label = job["label"]
            status = "Loaded" if label in loaded else "NOT LOADED"
            sched = job["schedule"]
            marker = "[OK]" if label in loaded else "[!!]"
            print(f"  {marker} {label:<37} {status:<14} {sched}")
        print()

    elif action == "reload":
        if not args.job:
            print("Error: specify a job to reload (gitbackup, onedrive, checkpoint)")
            sys.exit(1)
        job = _resolve_job(args.job)
        plist = str(job["plist"])
        label = job["label"]
        print(f"Reloading {label}...")
        subprocess.run(["launchctl", "bootout", f"gui/{os.getuid()}", plist], check=False)
        result = subprocess.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", plist], check=False)
        if result.returncode == 0:
            print("Reloaded successfully.")
        else:
            print(f"Reload failed (exit {result.returncode}). Trying legacy load...")
            subprocess.run(["launchctl", "unload", plist], check=False)
            subprocess.run(["launchctl", "load", plist], check=False)

    elif action == "logs":
        if not args.job:
            print("Error: specify a job (gitbackup, onedrive, checkpoint)")
            sys.exit(1)
        job = _resolve_job(args.job)
        for label, log_path in [("stdout", job["stdout_log"]), ("stderr", job["stderr_log"])]:
            print(f"\n--- {label}: {log_path} ---")
            if not log_path.exists():
                print("  (no log file)")
                continue
            lines = log_path.read_text().splitlines()
            tail = lines[-30:] if len(lines) > 30 else lines
            for line in tail:
                print(f"  {line}")
        print()

    else:
        print(f"Unknown launchctl action: {action}")
        sys.exit(1)


# ── CLI ──────────────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        prog="backup_agent",
        description="Backup Specialist Agent — monitor and manage the backup system",
    )
    sub = parser.add_subparsers(dest="command", help="Available commands")

    sub.add_parser("status", help="Show full backup system health report")

    run_p = sub.add_parser("run", help="Manually trigger a backup script")
    run_p.add_argument("target", choices=["git", "onedrive", "checkpoint", "all"])
    run_p.add_argument("--dry-run", action="store_true", help="Run without making changes")

    config_p = sub.add_parser("config", help="View or manage backup configuration")
    config_p.add_argument("action", choices=["show", "edit", "validate"])

    launch_p = sub.add_parser("launchctl", help="Manage LaunchAgent jobs")
    launch_p.add_argument("action", choices=["status", "reload", "logs"])
    launch_p.add_argument("job", nargs="?", help="Job name: gitbackup, onedrive, checkpoint")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    dispatch = {
        "status": cmd_status,
        "run": cmd_run,
        "config": cmd_config,
        "launchctl": cmd_launchctl,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
