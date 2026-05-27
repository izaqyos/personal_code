from __future__ import annotations

import json
import logging
import sys
import traceback
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import IO

LOGGER_NAME = "gam"

_OPTIONAL_KEYS = ("pr", "state", "screenshot", "duration_ms")
_ANSI = {
    "DEBUG": "\x1b[90m",
    "INFO": "\x1b[36m",
    "WARNING": "\x1b[33m",
    "ERROR": "\x1b[31m",
    "CRITICAL": "\x1b[1;31m",
    "RESET": "\x1b[0m",
}


@dataclass
class RunContext:
    """Shared context for a single `run` invocation."""

    run_id: str
    run_dir: Path
    authenticated_login: str | None = None
    screenshot_counters: dict[str, int] = field(default_factory=dict)


class JSONFormatter(logging.Formatter):
    """Emit one JSON object per log event matching the run.jsonl schema in spec §7.2."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict = {
            "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") +
                  f"{int(record.msecs):03d}Z",
            "level": record.levelname,
            "run_id": getattr(record, "run_id", None),
            "step": getattr(record, "step", None),
            "msg": record.getMessage(),
        }
        for key in _OPTIONAL_KEYS:
            val = getattr(record, key, None)
            if val is not None:
                payload[key] = val
        if record.exc_info:
            etype, evalue, etb = record.exc_info
            payload["exception"] = {
                "type": etype.__name__ if etype else "UnknownError",
                "repr": repr(evalue),
                "traceback": "".join(traceback.format_exception(etype, evalue, etb)),
            }
        return json.dumps(payload, ensure_ascii=False)


class ColorConsoleHandler(logging.StreamHandler):
    """Stream handler with ANSI level coloring and a human-readable layout.

    Format: `HH:MM:SS LEVEL [pr=… step=…] message`
    """

    def __init__(self, stream: IO[str] | None = None, *, use_color: bool | None = None):
        super().__init__(stream or sys.stdout)
        if use_color is None:
            use_color = bool(getattr(self.stream, "isatty", lambda: False)())
        self.use_color = use_color

    def format(self, record: logging.LogRecord) -> str:
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        bits = [ts, record.levelname]
        ctx_bits = []
        pr = getattr(record, "pr", None)
        step = getattr(record, "step", None)
        if pr:
            ctx_bits.append(f"pr={pr}")
        if step:
            ctx_bits.append(f"step={step}")
        if ctx_bits:
            bits.append("[" + " ".join(ctx_bits) + "]")
        bits.append(record.getMessage())
        line = " ".join(bits)
        if self.use_color:
            color = _ANSI.get(record.levelname, "")
            line = f"{color}{line}{_ANSI['RESET']}"
        if record.exc_info:
            line += "\n" + "".join(traceback.format_exception(*record.exc_info))
        return line


class _ContextFilter(logging.Filter):
    """Inject default RunContext fields onto every record."""

    def __init__(self, ctx: RunContext):
        super().__init__()
        self.ctx = ctx

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "run_id"):
            record.run_id = self.ctx.run_id
        return True


def make_run_logger(ctx: RunContext, *, verbose: bool, quiet: bool) -> logging.Logger:
    """Build the `gam` logger, attach JSON file + colored stdout handlers, install context filter."""
    logger = logging.getLogger(LOGGER_NAME)
    # Reset handlers on re-init so tests can call this repeatedly.
    for h in list(logger.handlers):
        logger.removeHandler(h)
    for f in list(logger.filters):
        logger.removeFilter(f)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    ctx.run_dir.mkdir(parents=True, exist_ok=True)
    file_h = logging.FileHandler(ctx.run_dir / "run.jsonl", encoding="utf-8")
    file_h.setLevel(logging.DEBUG)
    file_h.setFormatter(JSONFormatter())
    logger.addHandler(file_h)

    console_h = ColorConsoleHandler()
    if verbose:
        console_h.setLevel(logging.DEBUG)
    elif quiet:
        console_h.setLevel(logging.WARNING)
    else:
        console_h.setLevel(logging.INFO)
    logger.addHandler(console_h)

    logger.addFilter(_ContextFilter(ctx))
    return logger
