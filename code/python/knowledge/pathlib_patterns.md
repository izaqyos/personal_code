# Python pathlib Patterns

## Overview

Modern, object-oriented filesystem path handling with `pathlib` (Python 3.4+).

---

## 1. Basic Usage

```python
from pathlib import Path

# Current directory
cwd = Path.cwd()

# Home directory
home = Path.home()

# Script's directory (common pattern)
SCRIPT_DIR = Path(__file__).parent

# Absolute path from string
path = Path("/Users/yosii/work/file.txt")

# Relative path
path = Path("data/file.txt")
```

---

## 2. Path Construction

```python
# Join paths with /
base = Path("/Users/yosii")
full_path = base / "work" / "file.txt"
# Result: /Users/yosii/work/file.txt

# From parent
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
CONFIG_FILE = SCRIPT_DIR / "config.json"
```

---

## 3. Path Properties

```python
path = Path("/Users/yosii/work/project/file.txt")

path.name        # "file.txt"
path.stem        # "file" (without extension)
path.suffix      # ".txt"
path.parent      # Path("/Users/yosii/work/project")
path.parents[0]  # Same as parent
path.parents[1]  # Path("/Users/yosii/work")
path.parts       # ('/', 'Users', 'yosii', 'work', 'project', 'file.txt')
path.anchor      # "/" (root on Unix)
```

---

## 4. Checking Paths

```python
path = Path("file.txt")

path.exists()      # True if exists
path.is_file()     # True if file
path.is_dir()      # True if directory
path.is_symlink()  # True if symlink
path.is_absolute() # True if absolute path
```

---

## 5. File Operations

### Reading

```python
# Read text
content = Path("file.txt").read_text()
content = Path("file.txt").read_text(encoding="utf-8")

# Read bytes
data = Path("image.png").read_bytes()

# Read lines
lines = Path("file.txt").read_text().splitlines()
```

### Writing

```python
# Write text
Path("output.txt").write_text("Hello, World!")

# Write bytes
Path("output.bin").write_bytes(b"\x00\x01\x02")

# Write JSON
import json
Path("data.json").write_text(json.dumps(data, indent=2))
```

### With Context Manager

```python
# Standard file operations
with open(Path("file.txt")) as f:
    content = f.read()

# Or with path directly
with Path("file.txt").open() as f:
    content = f.read()
```

---

## 6. Directory Operations

### Create

```python
# Create directory (no error if exists)
Path("output").mkdir(exist_ok=True)

# Create nested directories
Path("a/b/c").mkdir(parents=True, exist_ok=True)
```

### List Contents

```python
# All items in directory
for item in Path("dir").iterdir():
    print(item)

# Only files
files = [f for f in Path("dir").iterdir() if f.is_file()]

# Only directories
dirs = [d for d in Path("dir").iterdir() if d.is_dir()]
```

### Glob Patterns

```python
# All .py files in directory
for py_file in Path("src").glob("*.py"):
    print(py_file)

# Recursive (all subdirectories)
for py_file in Path("src").rglob("*.py"):
    print(py_file)

# Multiple patterns
for file in Path(".").glob("**/*.{py,sh}"):  # Doesn't work!
    pass

# Correct way for multiple patterns
from itertools import chain
files = chain(Path(".").rglob("*.py"), Path(".").rglob("*.sh"))
```

---

## 7. Path Manipulation

### Change Extension

```python
path = Path("file.txt")
new_path = path.with_suffix(".json")  # file.json
no_ext = path.with_suffix("")         # file
```

### Change Name

```python
path = Path("/data/file.txt")
new_path = path.with_name("other.txt")    # /data/other.txt
new_stem = path.with_stem("other")        # /data/other.txt (Python 3.9+)
```

### Resolve and Absolute

```python
path = Path("../file.txt")
absolute = path.resolve()  # Resolves symlinks and ..
absolute = path.absolute() # Just makes absolute
```

---

## 8. File Management

```python
# Rename/move
Path("old.txt").rename("new.txt")
Path("old.txt").replace("new.txt")  # Overwrites if exists

# Delete
Path("file.txt").unlink()           # Delete file
Path("file.txt").unlink(missing_ok=True)  # No error if missing
Path("empty_dir").rmdir()           # Delete empty directory

# For non-empty directories, use shutil
import shutil
shutil.rmtree(Path("directory"))
```

---

## 9. Real Example: Data File Management

```python
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR / "data"
LATEST_DATA = DATA_DIR / "code_reviews_latest.json"

def load_data():
    """Load the latest data file."""
    if not LATEST_DATA.exists():
        print(f"❌ No data file found at {LATEST_DATA}")
        return None
    
    with open(LATEST_DATA) as f:
        return json.load(f)

def save_data(data: dict):
    """Save data with timestamp."""
    DATA_DIR.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = DATA_DIR / f"data_{timestamp}.json"
    
    output_file.write_text(json.dumps(data, indent=2))
    
    # Update symlink
    latest = DATA_DIR / "latest.json"
    if latest.is_symlink():
        latest.unlink()
    latest.symlink_to(output_file.name)  # Relative symlink
```

---

## 10. Common Patterns

### Get Script Directory

```python
# Best practice for scripts
SCRIPT_DIR = Path(__file__).parent.resolve()
```

### Config File Resolution

```python
def find_config():
    """Find config file, checking multiple locations."""
    locations = [
        Path.cwd() / "config.yaml",
        Path.home() / ".config" / "myapp" / "config.yaml",
        Path("/etc/myapp/config.yaml"),
    ]
    
    for loc in locations:
        if loc.exists():
            return loc
    return None
```

### Temporary Files with pathlib

```python
import tempfile

# Temp file
with tempfile.NamedTemporaryFile(suffix=".json") as f:
    temp_path = Path(f.name)
    temp_path.write_text('{"test": true}')

# Temp directory
with tempfile.TemporaryDirectory() as tmpdir:
    temp_path = Path(tmpdir) / "file.txt"
    temp_path.write_text("content")
```

---

## os.path vs pathlib

| os.path | pathlib |
|---------|---------|
| `os.path.join(a, b)` | `Path(a) / b` |
| `os.path.dirname(p)` | `Path(p).parent` |
| `os.path.basename(p)` | `Path(p).name` |
| `os.path.exists(p)` | `Path(p).exists()` |
| `os.path.isfile(p)` | `Path(p).is_file()` |
| `os.makedirs(p)` | `Path(p).mkdir(parents=True)` |
| `os.listdir(p)` | `list(Path(p).iterdir())` |
| `glob.glob("*.py")` | `Path().glob("*.py")` |

---

## See Also

- [pathlib docs](https://docs.python.org/3/library/pathlib.html)
- `~/work/CheckPoint/Jira/statistics/visualize_reviews.py` - Real example

---

**Created:** 2026-01-27  
**Source:** Code Review Statistics project
