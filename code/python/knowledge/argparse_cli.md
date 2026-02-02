# Python argparse CLI Patterns

## Overview

Building command-line interfaces with Python's `argparse` module.

---

## 1. Basic Structure

```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="Tool description shown in --help"
    )
    
    # Add arguments
    parser.add_argument("input", help="Input file path")
    
    # Parse
    args = parser.parse_args()
    
    print(f"Processing: {args.input}")

if __name__ == "__main__":
    main()
```

**Usage:**
```bash
python script.py myfile.txt
python script.py --help
```

---

## 2. Argument Types

### Positional (Required)

```python
parser.add_argument("filename", help="File to process")
```

### Optional with Value

```python
parser.add_argument("--output", "-o", help="Output file")
parser.add_argument("--count", "-c", type=int, default=10, help="Number of items")
```

### Boolean Flags

```python
parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
parser.add_argument("--quiet", "-q", action="store_false", dest="verbose")
```

### Choices (Restricted Values)

```python
parser.add_argument(
    "--format", 
    choices=["json", "csv", "xml"],
    default="json",
    help="Output format"
)

parser.add_argument(
    "--period",
    choices=["last_month", "last_3_months", "full_year"],
    default="full_year",
    help="Time period"
)
```

### Multiple Values

```python
parser.add_argument("--files", nargs="+", help="One or more files")
parser.add_argument("--tags", nargs="*", help="Zero or more tags")
```

---

## 3. Mutually Exclusive Groups

```python
group = parser.add_mutually_exclusive_group()
group.add_argument("--verbose", action="store_true")
group.add_argument("--quiet", action="store_true")
```

---

## 4. Subcommands

```python
parser = argparse.ArgumentParser(description="Git-like tool")
subparsers = parser.add_subparsers(dest="command", help="Commands")

# 'init' command
init_parser = subparsers.add_parser("init", help="Initialize repo")
init_parser.add_argument("--bare", action="store_true")

# 'commit' command
commit_parser = subparsers.add_parser("commit", help="Create commit")
commit_parser.add_argument("-m", "--message", required=True)

args = parser.parse_args()

if args.command == "init":
    initialize(bare=args.bare)
elif args.command == "commit":
    commit(message=args.message)
```

---

## 5. Real Example: Visualization CLI

```python
def main():
    parser = argparse.ArgumentParser(
        description="Visualize code review statistics"
    )
    
    parser.add_argument(
        "--fetch", 
        action="store_true", 
        help="Fetch fresh data first"
    )
    
    parser.add_argument(
        "--period", 
        choices=["last_month", "last_3_months", "h2_2025", "full_2025"],
        default="full_2025", 
        help="Period to display"
    )
    
    parser.add_argument(
        "--export", 
        choices=["png", "pdf"], 
        help="Export format"
    )
    
    parser.add_argument(
        "--chart", 
        choices=["bar", "pie", "comparison", "all"], 
        default="all",
        help="Chart type to display"
    )
    
    args = parser.parse_args()
    
    if args.fetch:
        fetch_data()
    
    if args.chart in ["bar", "all"]:
        plot_bar(period=args.period)
```

**Usage:**
```bash
python viz.py --fetch --period last_month --chart bar
python viz.py --export png
```

---

## 6. Help Text Formatting

```python
parser = argparse.ArgumentParser(
    description="Tool description",
    epilog="Example: python tool.py --input file.txt",
    formatter_class=argparse.RawDescriptionHelpFormatter
)
```

**With docstring:**
```python
parser = argparse.ArgumentParser(
    description=__doc__,  # Uses module docstring
    formatter_class=argparse.RawDescriptionHelpFormatter
)
```

---

## 7. Environment Variable Defaults

```python
import os

parser.add_argument(
    "--api-key",
    default=os.environ.get("API_KEY"),
    help="API key (default: $API_KEY)"
)
```

---

## 8. Validation

```python
def valid_date(s):
    """Validate date format YYYY-MM-DD."""
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return s
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date: {s}")

parser.add_argument("--start", type=valid_date, help="Start date (YYYY-MM-DD)")
```

---

## 9. Complete Template

```python
#!/usr/bin/env python3
"""
My CLI Tool - Does something useful.

Examples:
    python tool.py input.txt --output result.json
    python tool.py --verbose input.txt
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Positional
    parser.add_argument("input", help="Input file")
    
    # Options
    parser.add_argument("-o", "--output", help="Output file")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--format", choices=["json", "csv"], default="json")
    
    args = parser.parse_args()
    
    if args.verbose:
        print(f"Processing: {args.input}")
    
    # Your logic here
    result = process(args.input)
    
    if args.output:
        save(result, args.output, args.format)
    else:
        print(result)

if __name__ == "__main__":
    main()
```

---

## Common Patterns

| Pattern | Code |
|---------|------|
| Required option | `parser.add_argument("--name", required=True)` |
| Default value | `default="value"` |
| Type conversion | `type=int`, `type=float`, `type=Path` |
| Choices | `choices=["a", "b", "c"]` |
| Boolean flag | `action="store_true"` |
| Count (`-vvv`) | `action="count", default=0` |
| Suppress from help | `help=argparse.SUPPRESS` |

---

## See Also

- [argparse docs](https://docs.python.org/3/library/argparse.html)
- `~/work/CheckPoint/Jira/statistics/visualize_reviews.py` - Real example

---

**Created:** 2026-01-27  
**Source:** Code Review Statistics project
