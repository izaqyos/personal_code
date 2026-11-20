"""Render docs/presenter_guide.html → docs/presenter_guide.pdf with headless Chrome."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

html = HERE / "presenter_guide.html"
pdf = HERE / "presenter_guide.pdf"
proc = subprocess.run(
    [
        CHROME,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf}",
        html.as_uri(),
    ],
    capture_output=True,
    text=True,
    check=False,
)
if proc.returncode != 0 or not pdf.exists():
    sys.exit(f"chrome failed: {proc.stderr[-500:]}")
print(pdf)
