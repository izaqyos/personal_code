"""Banner-specific exception types."""


class BannerError(Exception):
    """Base class for banner-related errors."""


class MissingScheduleError(BannerError):
    """Raised when the schedules.json file cannot be located or read."""

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"schedules.json not found at: {path}")


class MalformedScheduleError(BannerError):
    """Raised when schedules.json exists but cannot be parsed/validated."""

    def __init__(self, reason: str) -> None:
        self.reason = reason
        super().__init__(f"malformed schedules.json: {reason}")
