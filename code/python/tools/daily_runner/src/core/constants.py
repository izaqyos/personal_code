"""
Shared constants for the Daily Standup Timer application.

This module centralizes magic numbers and configuration defaults
to ensure consistency across the codebase and make values
easy to modify.
"""

# =============================================================================
# Time Constants (in seconds)
# =============================================================================

# Default speaker time allocation
DEFAULT_SPEAKER_TIME_SECONDS = 180  # 3 minutes

# Minimum and maximum speaker time bounds
MIN_SPEAKER_TIME_SECONDS = 30
MAX_SPEAKER_TIME_SECONDS = 600  # 10 minutes

# Transition period between speakers
DEFAULT_TRANSITION_TIME_SECONDS = 5

# Grace period after timer expires (before auto-advance)
DEFAULT_GRACE_PERIOD_SECONDS = 15

# Overflow period after grace period (hard limit)
DEFAULT_OVERFLOW_PERIOD_SECONDS = 90

# Warning threshold - timer turns yellow
DEFAULT_WARNING_THRESHOLD_SECONDS = 30

# Time increment for +/- buttons
TIME_INCREMENT_SECONDS = 30

# Maximum meeting duration (safety limit)
MAX_MEETING_DURATION_SECONDS = 3600  # 1 hour

# Session ID display length (truncated UUID)
SESSION_ID_LENGTH = 8

# Keyboard input polling timeout
KEYBOARD_INPUT_TIMEOUT_SECONDS = 0.5

# Seconds per minute (for time calculations)
SECONDS_PER_MINUTE = 60

# Progress bar limits
PROGRESS_MIN = 0.0
PROGRESS_MAX = 1.0

# =============================================================================
# History Constants
# =============================================================================

# Default maximum history entries per team
DEFAULT_MAX_HISTORY_ENTRIES = 2000
MIN_HISTORY_ENTRIES = 100
MAX_HISTORY_ENTRIES = 10000

# =============================================================================
# Recovery Constants
# =============================================================================

# Auto-save interval for crash recovery
DEFAULT_AUTO_SAVE_INTERVAL_SECONDS = 10

# =============================================================================
# UI Constants
# =============================================================================

# Refresh rates
CLI_REFRESH_INTERVAL_SECONDS = 0.25  # 250ms - 4 refreshes per second
CLI_REFRESH_PER_SECOND = 4
STREAMLIT_REFRESH_INTERVAL_MS = 100

# Analytics default time range
DEFAULT_ANALYTICS_DAYS = 30

# =============================================================================
# Validation Constants
# =============================================================================

# Minimum length for generated IDs
MIN_ID_LENGTH = 10

# =============================================================================
# UI Styling Constants
# =============================================================================

# Font sizes for timer display
TIMER_FONT_SIZE_NORMAL = "2rem"
TIMER_FONT_SIZE_OVERFLOW = "2.5rem"

# CSS effects
OVERFLOW_TEXT_SHADOW = "0 0 10px #ff0000"
NO_TEXT_SHADOW = "none"

# =============================================================================
# Color Scheme (for UI components)
# =============================================================================

COLORS = {
    "normal": "#00ff00",      # Green - plenty of time
    "warning": "#ffff00",     # Yellow - approaching limit
    "overtime": "#ff0000",    # Red - exceeded time
    "overflow": "#ff0000",    # Bold red - hard overflow limit
    "paused": "#0066ff",      # Blue - timer paused
    "transition": "#00ffff",  # Cyan - between speakers
    "completed": "#888888",   # Gray - finished
    "current": "#ffffff",     # White - current speaker
    "pending": "#aaaaaa",     # Light gray - waiting
    "absent": "#ff6666",      # Light red - absent
    "skipped": "#ffaa66",     # Orange - skipped
}

# =============================================================================
# Logging Constants
# =============================================================================

# Log file settings
LOG_FILE_NAME = "daily_timer.log"
LOG_DIR = "logs"
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB max per file
LOG_BACKUP_COUNT = 3  # Keep 3 backup files (total ~20MB max)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
