"""Execute the runnable fences in wiki/playbook pages.

Fences tagged `python` and `ts` must run cleanly; `py` / `typescript` / others are illustrative.
Python snippets also have to pass ruff with the suite's rules.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

FENCE_RE = re.compile(r"^```(\w*)\s*$")
RUFF_RULES = "E,F,W,I,B,UP,SIM,C4,RET,PL,RUF,DTZ,ASYNC"
RUFF_IGNORE = "PLR2004,PLR0913,E501,PLC0415,I001,RUF005"  # snippets: inline literals, many kwargs, imports
NO_COLOR = {**os.environ, "NO_COLOR": "1"}


def runnable_blocks(text: str) -> list[tuple[str, int, str]]:
    """Return (lang, start_line, code) for `python` and `ts` fences."""
    out: list[tuple[str, int, str]] = []
    lang: str | None = None
    start, buf = 0, []
    for n, line in enumerate(text.splitlines(), start=1):
        m = FENCE_RE.match(line)
        if lang is None and m:
            lang, start, buf = m.group(1), n + 1, []
        elif lang is not None and line.startswith("```"):
            if lang in ("python", "ts"):
                out.append((lang, start, "\n".join(buf) + "\n"))
            lang = None
        elif lang is not None:
            buf.append(line)
    return out


def check_page(page: Path) -> list[str]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, (lang, line, code) in enumerate(runnable_blocks(page.read_text())):
            where = f"{page.name}:{line}"
            if lang == "python":
                f = Path(tmp, f"b{i}.py")
                f.write_text(code)
                lint = subprocess.run(
                    [
                        "ruff",
                        "check",
                        "--no-cache",
                        "--isolated",
                        "--select",
                        RUFF_RULES,
                        "--ignore",
                        RUFF_IGNORE,
                        "--output-format",
                        "concise",
                        str(f),
                    ],
                    capture_output=True,
                    text=True,
                    check=False,
                    env=NO_COLOR,
                )
                if lint.returncode != 0:
                    errors.append(f"{where} ruff: {lint.stdout.strip().splitlines()[0]}")
                cmd = [sys.executable, str(f)]
            else:
                if shutil.which("node") is None:
                    continue
                f = Path(tmp, f"b{i}.mts")
                f.write_text(code + "export {};\n")
                cmd = ["node", "--no-warnings", str(f)]
            run = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=60)
            if run.returncode != 0:
                errors.append(f"{where} {lang} failed: {(run.stderr or run.stdout).strip()[-300:]}")
    return errors


if __name__ == "__main__":
    problems = [e for p in sys.argv[1:] for e in check_page(Path(p))]
    print("\n".join(problems) or "all runnable snippets OK")
    sys.exit(1 if problems else 0)
