# Backup Specialist Agent

A unified CLI for monitoring and managing the personal backup system.

## Quick Start

```bash
# Using the venv python directly
~/work/git/git_backup/yosi_general_venv/bin/python backup_agent.py status

# Or via the launcher menu (option 8)
launcher
```

## Commands

### `status` — Full health check

```bash
python backup_agent.py status
```

Shows:
- LaunchAgent job status (loaded / not loaded)
- Last run timestamps from log files
- Git repo dirty state (uncommitted changes per repo)
- OneDrive archive count, total size, freshness
- Local Obsidian checkpoint backup count and age

### `run` — Manually trigger a backup

```bash
python backup_agent.py run git          # dotfiles + repos -> GitHub
python backup_agent.py run onedrive     # archives -> OneDrive cloud
python backup_agent.py run checkpoint   # Obsidian checkpoint snapshot
python backup_agent.py run all          # all three in sequence
python backup_agent.py run git --dry-run  # preview without changes
```

### `config` — View or manage configuration

```bash
python backup_agent.py config show      # display config summary
python backup_agent.py config edit      # open config.yaml in $EDITOR
python backup_agent.py config validate  # check all paths and plists exist
```

### `launchctl` — Manage scheduled jobs

```bash
python backup_agent.py launchctl status              # show job load status
python backup_agent.py launchctl reload gitbackup     # unload + reload plist
python backup_agent.py launchctl logs gitbackup       # tail last 30 lines of logs
```

Job names: `gitbackup`, `onedrive`, `checkpoint`

## Backup System Overview

| Component | Script | Schedule | Destination |
|-----------|--------|----------|-------------|
| Git backup | `backup.py` | Sun, Tue, Thu @ 15:30 | GitHub |
| OneDrive | `backup_to_onedrive.py` | Sun @ 16:00 | OneDrive cloud |
| Checkpoint | `backup_obsidian_checkpoint.py` | Sun @ 15:00 | Local disk |

## Dependencies

- Python 3 (via `~/work/git/git_backup/yosi_general_venv/`)
- PyYAML (for config parsing, installed in the venv)
- Existing backup scripts at `~/work/git/git_backup/`
- macOS launchctl (for LaunchAgent management)
