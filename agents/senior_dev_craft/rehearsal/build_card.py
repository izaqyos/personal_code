"""Render cheat-card.html -> cheat-card.pdf with headless Chrome; fail unless it is exactly 1 page."""

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

html, pdf = HERE / "cheat-card.html", HERE / "cheat-card.pdf"
proc = subprocess.run(
    [CHROME, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", html.as_uri()],
    capture_output=True,
    text=True,
    check=False,
)
if proc.returncode != 0 or not pdf.exists():
    sys.exit(f"chrome failed: {proc.stderr[-500:]}")
pages = len(re.findall(rb"/Type\s*/Page[^s]", pdf.read_bytes()))
if pages != 1:
    sys.exit(f"{pdf.name} has {pages} pages; trim the card to 1")
print(f"{pdf} (1 page)")
