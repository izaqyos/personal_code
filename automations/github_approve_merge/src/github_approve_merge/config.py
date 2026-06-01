from __future__ import annotations

import re
import secrets
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_RETENTION_DAYS = 10

RUN_ID_PATTERN = re.compile(r"^\d{8}-\d{6}-[a-f0-9]{4}$")


def default_logs_dir() -> Path:
    """`./logs` relative to the current working directory."""
    return Path.cwd() / "logs"


def generate_run_id() -> str:
    """`YYYYMMDD-HHMMSS-<rand4>` (UTC) — matches RUN_ID_PATTERN."""
    now = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{now}-{secrets.token_hex(2)}"
