# Cursor AI Usage Tracker

A Python script to monitor and manage your Cursor AI monthly request limit, helping you avoid hitting the 1000 request cap before the end of your billing period.

## Why Use This?

Cursor AI has different models with different costs:

- **Standard models**: 1 request per message (Claude 4 Sonnet, Haiku, etc.)
- **Premium models**: 4 requests per message (Claude 4 Opus, 4.1 Opus)

Without tracking, it's easy to burn through your 1000 monthly requests, especially if you use premium models frequently.

**Note:** This is a manual tracker. You need to sync your usage from Cursor's dashboard.

## Installation

### Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

### Setup

The script is ready to use:

```bash
python3 cursor_tracker.py
```

## Launcher

Interactive menu-driven launcher for frequently used scripts:

### Using the Launcher Script

The launcher provides an interactive menu system and is available globally via PATH:

```bash
# Run the launcher from anywhere (after adding to PATH)
launcher.sh

# Or with full path
/Users/yosii/work/git/personal_code/code/bash/launcher.sh
```

**Note:** The launcher script is located at `/Users/yosii/work/git/personal_code/code/bash/launcher.sh` and has been added to your PATH in both `.zshrc` and `.bashrc`. You may need to restart your terminal or run `source ~/.zshrc` (or `source ~/.bashrc`) for the PATH changes to take effect.

**Main Menu:**
- **1** - Cursor Tracker
- **2** - Remind Champion
- **3** - Repo Cleaner
- **0** - Exit

**Cursor Tracker Submenu:**
- **1** - Show Status
- **2** - Add Usage
- **3** - View History
- **4** - Reset Counter
- **5** - Show Help
- **0** - Back to Main Menu

**Remind Champion Submenu:**
- **1** - Show Release Schedule
- **2** - Show DoD Schedule
- **3** - Show All Schedules
- **4** - Send DoD Reminder
- **5** - Send TL DoD Reminder
- **6** - Cron Mode (Auto-send)
- **7** - Validate Schedules
- **8** - View Reminder Log
- **9** - List Reminder Types
- **10** - List Team Members
- **11** - Check DoD for Date
- **0** - Back to Main Menu

**Repo Cleaner Submenu:**
- **1** - Current Directory (Dry Run)
- **2** - Current Directory (Clean)
- **3** - Specific Directory (Dry Run)
- **4** - Specific Directory (Clean)
- **5** - View Cleanup History
- **6** - List Available Languages
- **0** - Back to Main Menu

### Direct Commands (Alternative)

You can still use direct commands if preferred:

```bash
# View current status (most common)
python3 cursor_tracker.py

# Add standard usage (50 requests)
python3 cursor_tracker.py add 50

# Add premium model usage (2 messages = 8 requests)
python3 cursor_tracker.py add 2 claude-4-opus

# View usage history
python3 cursor_tracker.py history

# Reset counter (monthly reset)
python3 cursor_tracker.py reset

# Show help
python3 cursor_tracker.py help
```

## Usage

### View Current Status

```bash
python3 cursor_tracker.py
```

Example output:

```
============================================================
  🟢 CURSOR AI USAGE TRACKER 🟢
============================================================

🕐 LAST UPDATE
   December 15, 2025 at 14:30 (2 days ago)

📊 USAGE OVERVIEW
   Used:        320 / 1000 requests (32.0%)
   Remaining:   680 requests
   [████████████████░░░░░░░░░░░░░░░░░░░░░░░░]

📅 TIME
   Days elapsed:   10
   Days remaining: 21
   Resets on:      January 01, 2026

🎯 BUDGET
   Original daily budget: 32.3 requests/day
   Adjusted daily budget: 32.4 requests/day
   Status: ON TRACK ✅

💡 RECOMMENDATION
   ✅ Use any model comfortably

------------------------------------------------------------
📝 SYNC WITH REAL USAGE
   Check actual usage: https://cursor.com/dashboard?tab=usage
   Then run: python3 cursor_tracker.py add <count>
============================================================
```

### Add Usage

Sync your usage from Cursor's dashboard:

```bash
# Add standard model requests (1 request each)
python3 cursor_tracker.py add 50

# Add premium model requests (4 requests each)
python3 cursor_tracker.py add 2 claude-4-opus
```

### View History

```bash
python3 cursor_tracker.py history
```

Example output:

```
============================================================
  📜 USAGE HISTORY
============================================================
   Dec 15 14:30 | + 50 req | standard             | Total: 50
   Dec 16 09:15 | +  8 req | claude-4-opus        | Total: 58
   Dec 17 11:00 | + 25 req | standard             | Total: 83
============================================================
```

### Reset Counter

On the 1st of each month (when Cursor resets your limit):

```bash
python3 cursor_tracker.py reset
```

### Get Help

```bash
python3 cursor_tracker.py help
```

## Supported Models

| Model | Cost per Message |
|-------|------------------|
| Claude 4 Sonnet | 1 request |
| Claude 4.5 Sonnet | 1 request |
| Claude 4.5 Haiku | 1 request |
| Claude 4.5 Opus | 1 request |
| Composer I | 1 request |
| Gemini models | 1 request |
| Claude 4 Opus | 4 requests |
| Claude 4.1 Opus | 4 requests |

## Configuration

Edit the script to customize:

```python
# At the top of cursor_tracker.py
MONTHLY_LIMIT = 1000        # Your monthly request limit
RESET_DAY = 1               # Day of month when limit resets
MAX_HISTORY_ENTRIES = 500   # Keep last N history entries
```

## Data Storage

Usage data is stored in `usage_statistics.json` (same directory as the script).

```json
{
  "total_used": 58,
  "last_updated": "2025-12-17T11:00:00",
  "reset_date": "2026-01-01T00:00:00",
  "history": [
    {"timestamp": "...", "requests": 50, "model": "standard", "cost": 50, "total_after": 50},
    {"timestamp": "...", "requests": 2, "model": "claude-4-opus", "cost": 8, "total_after": 58}
  ]
}
```

### History Cleanup

- History automatically trims to the last 500 entries (configurable via `MAX_HISTORY_ENTRIES`)
- History is cleared on `reset` command

## Usage Strategy

### Green Zone (0-50% used)

- Use any model freely
- Experiment with premium models for complex tasks

### Yellow Zone (50-75% used)

- Prefer standard models for routine tasks
- Reserve premium models for critical work only

### Red Zone (75-100% used)

- ONLY use standard models (1 request each)
- Avoid premium models entirely

## Troubleshooting

### Lost track of actual usage

Check your actual usage on Cursor's dashboard:
https://cursor.com/dashboard?tab=usage

Then sync:

```bash
python3 cursor_tracker.py reset
python3 cursor_tracker.py add <your_actual_usage>
```

### Script shows wrong dates

The script auto-detects when a new month starts. If dates seem wrong:

```bash
python3 cursor_tracker.py reset
```

## License

MIT License - Free to use and modify
