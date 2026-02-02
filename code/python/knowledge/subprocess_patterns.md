# Python Subprocess Patterns

## Overview

Patterns for running external commands from Python, with proper error handling.

---

## 1. Basic Run with Capture

```python
import subprocess

result = subprocess.run(
    ["ls", "-la"],
    capture_output=True,  # Capture stdout and stderr
    text=True,            # Return strings, not bytes
    timeout=30            # Fail if command takes > 30s
)

if result.returncode == 0:
    print(result.stdout)
else:
    print(f"Error: {result.stderr}")
```

**Key Points:**
- `capture_output=True` is shorthand for `stdout=PIPE, stderr=PIPE`
- `text=True` decodes output as UTF-8 (Python 3.7+)
- Always check `returncode`

---

## 2. Running Shell Scripts

```python
from pathlib import Path

script = Path(__file__).parent / "my_script.sh"
result = subprocess.run(
    ["bash", str(script)],
    capture_output=True,
    text=True
)
```

**Why explicit `bash`:**
- Ensures script runs in bash, not sh
- Works even if script isn't executable
- Cross-platform (Windows needs explicit shell)

---

## 3. Checking for Command Existence

```python
def command_exists(cmd: str) -> bool:
    """Check if a command is available in PATH."""
    result = subprocess.run(
        ["which", cmd],
        capture_output=True,
        text=True
    )
    return result.returncode == 0
```

**Alternative using `shutil`:**
```python
import shutil
exists = shutil.which("gh") is not None
```

---

## 4. JSON Output from CLI Tools

```python
import json
import subprocess

def get_gh_user() -> dict:
    """Get GitHub user info via gh CLI."""
    result = subprocess.run(
        ["gh", "api", "user", "--jq", ".login"],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"gh failed: {result.stderr}")
    
    return result.stdout.strip()

# For JSON output:
def get_prs() -> list:
    result = subprocess.run(
        ["gh", "search", "prs", "--json", "number,title"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []
```

---

## 5. Error Handling Patterns

### Silent Failure (Return Default)

```python
def safe_run(cmd: list, default="") -> str:
    """Run command, return default on failure."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        return result.stdout if result.returncode == 0 else default
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return default
```

### Fail Fast

```python
result = subprocess.run(cmd, check=True)  # Raises CalledProcessError on non-zero exit
```

---

## 6. Real Example: Code Review Fetcher

```python
def fetch_review_count(username: str, start: str, end: str) -> int:
    """Fetch PR review count from GitHub."""
    try:
        cmd = [
            "gh", "search", "prs",
            f"--reviewed-by={username}",
            f"--created={start}..{end}",
            "--limit=500",
            "--json", "number"
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            prs = json.loads(result.stdout)
            return len(prs)
        return 0
    except Exception:
        return 0
```

---

## Common Gotchas

| Problem | Solution |
|---------|----------|
| `FileNotFoundError` | Command not in PATH, use full path |
| Hanging forever | Always set `timeout` |
| Binary output | Use `text=True` for strings |
| Shell features (`|`, `>`) | Use `shell=True` (security risk!) |
| Windows paths | Use `Path` objects, convert with `str()` |

---

## See Also

- [subprocess docs](https://docs.python.org/3/library/subprocess.html)
- `~/work/CheckPoint/Jira/statistics/visualize_reviews.py` - Real-world example

---

**Created:** 2026-01-27  
**Source:** Code Review Statistics project
