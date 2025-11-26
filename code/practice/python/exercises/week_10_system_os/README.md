# Week 10: System & OS Programming

Master system programming with Python's standard library.

## Overview

This week focuses on system-level programming - working with the operating system, processes, environment variables, file systems, and system utilities. Learn essential modules for building robust system tools.

## Daily Breakdown

### Day 1: os and sys modules
- Environment variables
- Process management
- System information
- Command-line arguments
- Exit codes

### Day 2: subprocess
- Running external commands
- Pipes and redirection
- Process communication
- Error handling
- Shell vs direct execution

### Day 3: File System Operations
- shutil for file operations
- tempfile for temporary files
- File copying and moving
- Directory trees
- Disk usage

### Day 4: datetime and time
- Date and time objects
- Timezones and UTC
- Formatting and parsing
- Time calculations
- Performance timing

### Day 5: Platform and System Info
- platform module
- System detection
- Cross-platform code
- Hardware information
- OS-specific features

### Day 6: Signal Handling
- Signal basics
- Graceful shutdown
- Timeout handling
- Process control
- Unix signals

### Day 7: Review & Challenge
- System monitoring tool
- File backup utility
- Process manager
- Log rotation
- Complete system tools

## Key Modules

| Module | Purpose |
|--------|---------|
| `os` | Operating system interface |
| `sys` | System-specific parameters |
| `subprocess` | Spawn processes |
| `shutil` | High-level file operations |
| `tempfile` | Temporary files/directories |
| `datetime` | Date and time |
| `time` | Time access and conversions |
| `platform` | Platform identification |
| `signal` | Signal handling |

## Quick Reference

```python
import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Environment variables
api_key = os.getenv('API_KEY', 'default')
os.environ['MY_VAR'] = 'value'

# Run commands
result = subprocess.run(['ls', '-l'], capture_output=True, text=True)
print(result.stdout)

# File operations
shutil.copy('source.txt', 'dest.txt')
shutil.copytree('src_dir', 'dest_dir')
shutil.rmtree('dir_to_remove')

# Temporary files
import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    # Use tmpdir
    pass

# Date and time
now = datetime.now()
formatted = now.strftime('%Y-%m-%d %H:%M:%S')
parsed = datetime.strptime('2024-03-15', '%Y-%m-%d')

# Platform info
import platform
print(platform.system())  # 'Linux', 'Darwin', 'Windows'
print(platform.python_version())
```

## Learning Outcomes

✅ Work with environment variables  
✅ Run external commands  
✅ Manage files and directories  
✅ Handle dates and times  
✅ Write cross-platform code  
✅ Implement signal handling  
✅ Build system tools  

## Next Steps

🎯 **Week 11:** Concurrency  
Learn threading and multiprocessing.

---

*Build powerful system tools with Python! 🐍*

