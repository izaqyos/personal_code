import io
import json
import logging
from pathlib import Path

from github_approve_merge.logging_setup import (
    ColorConsoleHandler,
    JSONFormatter,
    RunContext,
    make_run_logger,
)


class TestJsonFormatter:
    def test_basic_event_shape(self):
        fmt = JSONFormatter()
        rec = logging.LogRecord(
            name="gam", level=logging.INFO, pathname=__file__, lineno=1,
            msg="hello", args=(), exc_info=None,
        )
        rec.run_id = "20260526-143012-7af3"
        rec.step = "after-load"
        out = fmt.format(rec)
        payload = json.loads(out)
        assert payload["msg"] == "hello"
        assert payload["level"] == "INFO"
        assert payload["run_id"] == "20260526-143012-7af3"
        assert payload["step"] == "after-load"
        assert payload["ts"].endswith("Z")
        assert "T" in payload["ts"]  # ISO 8601

    def test_extra_fields_are_included(self):
        fmt = JSONFormatter()
        rec = logging.LogRecord(
            name="gam", level=logging.INFO, pathname=__file__, lineno=1,
            msg="approved", args=(), exc_info=None,
        )
        rec.run_id = "rid"
        rec.step = "approve"
        rec.pr = "owner/repo#1"
        rec.state = "OPEN_APPROVABLE"
        rec.screenshot = "screenshots/foo.png"
        rec.duration_ms = 123
        payload = json.loads(fmt.format(rec))
        assert payload["pr"] == "owner/repo#1"
        assert payload["state"] == "OPEN_APPROVABLE"
        assert payload["screenshot"] == "screenshots/foo.png"
        assert payload["duration_ms"] == 123

    def test_exception_serialized(self):
        fmt = JSONFormatter()
        try:
            raise RuntimeError("kaboom")
        except RuntimeError:
            import sys
            exc_info = sys.exc_info()
        rec = logging.LogRecord(
            name="gam", level=logging.ERROR, pathname=__file__, lineno=1,
            msg="oops", args=(), exc_info=exc_info,
        )
        rec.run_id = "rid"
        rec.step = "bang"
        payload = json.loads(fmt.format(rec))
        assert payload["exception"]["type"] == "RuntimeError"
        assert "kaboom" in payload["exception"]["repr"]
        assert "Traceback" in payload["exception"]["traceback"]


class TestColorConsoleHandler:
    def test_format_contains_pr_and_step(self):
        h = ColorConsoleHandler(stream=io.StringIO(), use_color=False)
        rec = logging.LogRecord(
            name="gam", level=logging.INFO, pathname=__file__, lineno=1,
            msg="approve submitted", args=(), exc_info=None,
        )
        rec.run_id = "rid"
        rec.pr = "owner/repo#1"
        rec.step = "approve"
        line = h.format(rec)
        assert "approve submitted" in line
        assert "pr=owner/repo#1" in line
        assert "step=approve" in line
        assert "INFO" in line


class TestMakeRunLogger:
    def test_writes_jsonl_to_run_dir(self, tmp_path: Path):
        run_dir = tmp_path / "20260526-143012-7af3"
        run_dir.mkdir()
        ctx = RunContext(run_id="20260526-143012-7af3", run_dir=run_dir)
        logger = make_run_logger(ctx, verbose=False, quiet=True)
        logger.info("hello world", extra={"step": "boot"})

        line = (run_dir / "run.jsonl").read_text().splitlines()[0]
        payload = json.loads(line)
        assert payload["msg"] == "hello world"
        assert payload["step"] == "boot"
        assert payload["run_id"] == "20260526-143012-7af3"
