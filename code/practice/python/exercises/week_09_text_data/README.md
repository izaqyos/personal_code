# Week 9: Standard Library - Text & Data

Master Python's standard library for text processing and data manipulation.

## Overview

This week focuses on essential standard library modules for working with text and data. Learn regex, string formatting, JSON/CSV processing, path manipulation, I/O streams, and building command-line tools.

## Daily Breakdown

### Day 1: Regular Expressions (re module)
**File:** `day1_regex.py`

Master pattern matching:
- Basic regex patterns
- Special characters (. * + ? ^ $ [] {} () | \\)
- Groups and capturing
- Substitution with `re.sub()`
- Splitting with `re.split()`
- Validation patterns

**Key Patterns:**
- `\d`: digit, `\w`: word char, `\s`: whitespace
- `^`: start, `$`: end
- `*`: 0+, `+`: 1+, `?`: 0-1

---

### Day 2: String Formatting & Templates
**File:** `day2_string_formatting.py`

Professional string formatting:
- F-strings (Python 3.6+)
- `str.format()` method
- `string.Template` for safety
- Alignment and padding
- Number formatting
- Table formatting

**When to Use:**
- F-strings: Fast, readable, code-controlled
- format(): Dynamic, compatibility
- Template: User-provided strings (safe)

---

### Day 3: JSON and CSV Processing
**File:** `day3_json_csv.py`

Structured data handling:
- JSON encoding/decoding
- Custom JSON encoders
- CSV reading/writing
- DictReader and DictWriter
- Data format conversion
- Validation

**Complexity:**
- JSON: O(n) encoding/decoding
- CSV: O(n) streaming friendly

---

### Day 4: Path Manipulation (pathlib)
**File:** `day4_pathlib.py`

Modern path handling:
- `Path` object basics
- Path operations with `/` operator
- File system navigation
- `glob()` and `rglob()`
- Cross-platform paths
- File organization

**Advantages over os.path:**
- Object-oriented
- Chainable operations
- More readable

---

### Day 5: I/O and Streams
**File:** `day5_io_streams.py`

In-memory streams:
- `StringIO` for text
- `BytesIO` for binary
- Stream operations (seek, tell, read)
- Redirecting output
- File modes and buffering
- Text vs binary mode

**Use Cases:**
- Testing
- String building
- Protocol implementation

---

### Day 6: Command-Line Arguments & Logging
**File:** `day6_argparse_logging.py`

Professional CLI tools:
- `argparse` for argument parsing
- Positional and optional arguments
- Subcommands
- `logging` module
- Log levels and configuration
- File logging

**Log Levels:**
DEBUG < INFO < WARNING < ERROR < CRITICAL

---

### Day 7: Review & Challenge
**File:** `day7_review_challenge.py`

Apply all concepts:
- **Challenge 1:** Log analyzer
- **Challenge 2:** Data format converter
- **Challenge 3:** File processor CLI
- **Challenge 4:** Text statistics
- **Challenge 5:** Configuration manager
- **Challenge 6:** Path utilities
- **Challenge 7:** Complete data pipeline

---

## Quick Reference

### Regex Patterns

```python
import re

# Find all matches
emails = re.findall(r'\b[\w.-]+@[\w.-]+\.\w+\b', text)

# Search for pattern
match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
if match:
    year, month, day = match.groups()

# Substitute
cleaned = re.sub(r'\s+', ' ', text)

# Split
parts = re.split(r'[,;:]', text)
```

### String Formatting

```python
# F-strings (preferred)
name, age = "Alice", 30
print(f"{name} is {age} years old")
print(f"Pi: {3.14159:.2f}")
print(f"{'left':<10} {'right':>10}")

# format() method
"{} is {} years old".format(name, age)
"{name} is {age} years old".format(name=name, age=age)

# Template (safe for user input)
from string import Template
t = Template("Hello, $name!")
t.substitute(name=name)
```

### JSON and CSV

```python
import json
import csv

# JSON
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data, indent=2)
loaded = json.loads(json_str)

# CSV
with open('data.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerow({'name': 'Alice', 'age': 30})
```

### pathlib

```python
from pathlib import Path

# Create paths
p = Path('/home/user/file.txt')
p = Path.home() / 'documents' / 'file.txt'

# Properties
p.name          # 'file.txt'
p.stem          # 'file'
p.suffix        # '.txt'
p.parent        # Path('/home/user/documents')

# Operations
p.exists()
p.is_file()
p.is_dir()
p.read_text()
p.write_text('content')

# Iteration
for file in Path('.').glob('*.py'):
    print(file)
```

### Argparse & Logging

```python
import argparse
import logging

# Argparse
parser = argparse.ArgumentParser(description='My tool')
parser.add_argument('input', help='Input file')
parser.add_argument('--verbose', '-v', action='store_true')
args = parser.parse_args()

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.info("Application started")
logger.error("An error occurred")
```

---

## Module Comparison

| Task | Module | Best For |
|------|--------|----------|
| **Pattern matching** | `re` | Text validation, extraction |
| **String formatting** | f-strings | Code-controlled output |
| **Safe templates** | `string.Template` | User-provided templates |
| **Nested data** | `json` | APIs, configuration |
| **Tabular data** | `csv` | Spreadsheets, exports |
| **Path handling** | `pathlib` | File system operations |
| **In-memory I/O** | `io` | Testing, string building |
| **CLI parsing** | `argparse` | Command-line tools |
| **Logging** | `logging` | Application logging |

---

## Best Practices

### Regex
- Use raw strings: `r'pattern'`
- Compile patterns used repeatedly
- Avoid catastrophic backtracking
- Test patterns thoroughly

### String Formatting
- Use f-strings for code
- Use Template for user input
- Avoid concatenation in loops
- Use appropriate precision

### JSON/CSV
- Validate data after parsing
- Handle encoding (UTF-8)
- Stream large files
- Use DictReader/DictWriter

### pathlib
- Use pathlib over os.path
- Use `/` operator for joining
- Handle cross-platform differences
- Validate user-provided paths

### Logging
- Use appropriate log levels
- Don't log sensitive data
- Rotate log files
- Configure once at startup

---

## Learning Outcomes

After completing Week 9, you should be able to:

✅ Write and use regex patterns  
✅ Format strings professionally  
✅ Process JSON and CSV data  
✅ Manipulate paths with pathlib  
✅ Work with I/O streams  
✅ Build command-line tools  
✅ Implement proper logging  
✅ Build complete data pipelines  

---

## Running the Exercises

```bash
# Run individual days
python day1_regex.py
python day2_string_formatting.py
python day3_json_csv.py
python day4_pathlib.py
python day5_io_streams.py
python day6_argparse_logging.py
python day7_review_challenge.py

# Run all
for day in day*.py; do python "$day"; done
```

---

## Additional Resources

**Official Documentation:**
- [re module](https://docs.python.org/3/library/re.html)
- [string module](https://docs.python.org/3/library/string.html)
- [json module](https://docs.python.org/3/library/json.html)
- [csv module](https://docs.python.org/3/library/csv.html)
- [pathlib](https://docs.python.org/3/library/pathlib.html)
- [io module](https://docs.python.org/3/library/io.html)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [logging](https://docs.python.org/3/library/logging.html)

**Further Reading:**
- [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)
- [Logging Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)

---

## Next Steps

🎯 **Week 10:** System & OS  
Learn system programming with Python's standard library.

---

## Notes

- These modules are essential for real-world Python
- Master regex for text processing
- Use pathlib for modern path handling
- Always use logging over print in production
- Build robust CLI tools with argparse

**Time Investment:** ~10-15 minutes per day, 15-20 minutes for Day 7  
**Total:** ~90 minutes for the week

---

*Master Python's standard library for professional development! 🐍*

