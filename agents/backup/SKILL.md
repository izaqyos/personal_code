# Backup Specialist Agent

## When to Use

Use this skill when the user asks about:
- Backup status, health, or diagnostics
- Running backups manually (git, OneDrive, Obsidian checkpoint)
- LaunchAgent / launchctl job status for backup jobs
- Backup configuration or validation
- Whether their data is properly backed up
- Phrases like: "check backup status", "run backup", "backup health", "are my backups running", "backup logs"

## Overview

The backup system consists of three scheduled scripts managed by macOS LaunchAgents:

| Job | Script | Schedule |
|-----|--------|----------|
| `com.yosii.gitbackup` | `backup.py` | Sun, Tue, Thu @ 15:30 |
| `com.yosii.onedrive.backup` | `backup_to_onedrive.py` | Sun @ 16:00 |
| `com.yosii.obsidian.checkpoint` | `backup_obsidian_checkpoint.py` | Sun @ 15:00 |

Scripts live at `/Users/yosii/work/git/git_backup/`.
The agent CLI lives at `/Users/yosii/work/git/personal_code/agents/backup/backup_agent.py`.

## How to Use

### Step 1: Run status check first

```bash
/Users/yosii/work/git/git_backup/yosi_general_venv/bin/python /Users/yosii/work/git/personal_code/agents/backup/backup_agent.py status
```

This shows:
- LaunchAgent job status (loaded/running)
- Last run timestamps from logs
- Git repo dirty/clean state and uncommitted change counts
- OneDrive backup archive freshness and total size
- Local Obsidian checkpoint backup count and age

### Step 2: Diagnose issues from output

- `[!!]` = critical issue (job not loaded, backups very stale)
- `[!]` = warning (uncommitted changes, approaching staleness)
- `[OK]` = healthy

### Step 3: Take action if needed

```bash
# Run specific backup manually
python backup_agent.py run git
python backup_agent.py run onedrive
python backup_agent.py run checkpoint
python backup_agent.py run all

# Dry run (no changes)
python backup_agent.py run git --dry-run

# Check LaunchAgent jobs
python backup_agent.py launchctl status
python backup_agent.py launchctl logs gitbackup
python backup_agent.py launchctl reload gitbackup

# View/validate config
python backup_agent.py config show
python backup_agent.py config validate
```

### Step 4: Check logs for failures

```bash
python backup_agent.py launchctl logs gitbackup
python backup_agent.py launchctl logs onedrive
python backup_agent.py launchctl logs checkpoint
```

## Key Paths

- Backup scripts: `/Users/yosii/work/git/git_backup/`
- Config: `/Users/yosii/work/git/git_backup/config.yaml`
- Logs: `/Users/yosii/work/git/git_backup/logs/`
- Venv: `/Users/yosii/work/git/git_backup/yosi_general_venv/`
- LaunchAgents: `~/Library/LaunchAgents/com.yosii.*.plist`
- OneDrive backups: `~/Library/CloudStorage/OneDrive-CheckPointSoftwareTechnologiesLtd/Backups/`
- Obsidian checkpoints: `/Users/yosii/work/backup/obsidian/`
