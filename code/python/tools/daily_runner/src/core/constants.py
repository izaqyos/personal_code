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

# Warning threshold - timer turns yellow
DEFAULT_WARNING_THRESHOLD_SECONDS = 30

# Time increment for +/- buttons
TIME_INCREMENT_SECONDS = 30

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
CLI_REFRESH_INTERVAL_SECONDS = 0.1  # 100ms
CLI_REFRESH_PER_SECOND = 10
STREAMLIT_REFRESH_INTERVAL_MS = 100

# Analytics default time range
DEFAULT_ANALYTICS_DAYS = 30

# =============================================================================
# Validation Constants
# =============================================================================

# Minimum length for generated IDs
MIN_ID_LENGTH = 10

# =============================================================================
# Color Scheme (for UI components)
# =============================================================================

COLORS = {
    "normal": "#00ff00",      # Green - plenty of time
    "warning": "#ffff00",     # Yellow - approaching limit
    "overtime": "#ff0000",    # Red - exceeded time
    "paused": "#0066ff",      # Blue - timer paused
    "transition": "#00ffff",  # Cyan - between speakers
    "completed": "#888888",   # Gray - finished
    "current": "#ffffff",     # White - current speaker
    "pending": "#aaaaaa",     # Light gray - waiting
    "absent": "#ff6666",      # Light red - absent
    "skipped": "#ffaa66",     # Orange - skipped
}
