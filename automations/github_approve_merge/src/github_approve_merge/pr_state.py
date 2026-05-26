from __future__ import annotations

from enum import Enum, auto


class PRState(Enum):
    """Terminal classification of a PR's current state. See spec §9."""

    MERGED = auto()
    CLOSED = auto()
    DRAFT = auto()
    LOCKED = auto()
    SELF_AUTHORED = auto()
    CONFLICT = auto()
    REQUIRED_FAILING = auto()
    REQUIRED_PENDING = auto()
    OPEN_MERGEABLE = auto()
    OPEN_APPROVABLE = auto()


class StateFlag(Enum):
    """Modifier flags that combine with a PRState. See spec §9."""

    ALREADY_APPROVED = auto()
