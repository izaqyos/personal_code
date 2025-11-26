"""
Week 10, Day 7: Review & Challenge - System & OS Programming

Learning Objectives:
- Review all Week 10 concepts
- Apply system programming techniques
- Build practical system tools
- Master OS interaction
- Create complete utilities

Challenge: Build system monitoring and management tools

Time: 15-20 minutes
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import tempfile

# ============================================================
# REVIEW: Week 10 Concepts
# ============================================================

def week10_review():
    """Quick review of all Week 10 concepts"""
    print("=" * 60)
    print("WEEK 10 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: os and sys")
    print("  • Environment variables")
    print("  • System information")
    print("  • Command-line arguments")
    
    print("\nDay 2: subprocess")
    print("  • Running external commands")
    print("  • Process communication")
    print("  • Error handling")
    
    print("\nDay 3: File System")
    print("  • shutil for file operations")
    print("  • tempfile for temporary files")
    print("  • Directory management")
    
    print("\nDay 4: datetime and time")
    print("  • Date and time objects")
    print("  • Formatting and parsing")
    print("  • Time calculations")
    
    print("\nDay 5: Platform")
    print("  • System detection")
    print("  • Cross-platform code")
    print("  • Hardware information")
    
    print("\nDay 6: Signal Handling")
    print("  • Signal basics")
    print("  • Graceful shutdown")
    print("  • Process control")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: System Information Tool
# ============================================================

def system_info_tool():
    """
    Comprehensive system information display.
    """
    print("--- Challenge 1: System Information Tool ---")
    
    print("=" * 60)
    print("SYSTEM INFORMATION")
    print("=" * 60)
    
    # Python info
    print("\n[Python]")
    print(f"Version: {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")
    print(f"Platform: {sys.platform}")
    
    # System info
    print("\n[System]")
    print(f"Current Directory: {os.getcwd()}")
    print(f"Home Directory: {Path.home()}")
    print(f"Process ID: {os.getpid()}")
    
    # Environment
    print("\n[Environment]")
    print(f"Total Variables: {len(os.environ)}")
    print(f"PATH entries: {len(os.getenv('PATH', '').split(os.pathsep))}")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 2: File Backup Utility
# ============================================================

def file_backup_utility():
    """
    Create file backup with timestamp.
    """
    print("--- Challenge 2: File Backup Utility ---")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create test file
        source_file = tmp_path / "important.txt"
        source_file.write_text("Important data")
        
        # Create backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{source_file.stem}_{timestamp}{source_file.suffix}"
        backup_file = tmp_path / "backups" / backup_name
        
        backup_file.parent.mkdir(exist_ok=True)
        shutil.copy2(source_file, backup_file)
        
        print(f"Source: {source_file.name}")
        print(f"Backup: {backup_file.relative_to(tmp_path)}")
        print(f"Backup exists: {backup_file.exists()}")
        print(f"Size: {backup_file.stat().st_size} bytes")
    
    print()

# ============================================================
# CHALLENGE 3: Directory Statistics
# ============================================================

def directory_statistics():
    """
    Analyze directory contents.
    """
    print("--- Challenge 3: Directory Statistics ---")
    
    cwd = Path.cwd()
    print(f"Analyzing: {cwd}")
    
    try:
        items = list(cwd.iterdir())
        files = [item for item in items if item.is_file()]
        dirs = [item for item in items if item.is_dir()]
        
        print(f"\nStatistics:")
        print(f"  Total items: {len(items)}")
        print(f"  Files: {len(files)}")
        print(f"  Directories: {len(dirs)}")
        
        if files:
            total_size = sum(f.stat().st_size for f in files)
            print(f"  Total size: {total_size:,} bytes")
            
            # Largest file
            largest = max(files, key=lambda f: f.stat().st_size)
            print(f"  Largest file: {largest.name} ({largest.stat().st_size:,} bytes)")
    
    except PermissionError:
        print("Permission denied")
    
    print()

# ============================================================
# CHALLENGE 4: Environment Manager
# ============================================================

def environment_manager():
    """
    Manage environment variables.
    """
    print("--- Challenge 4: Environment Manager ---")
    
    # Set test variables
    test_vars = {
        'APP_NAME': 'MyApp',
        'APP_VERSION': '1.0.0',
        'APP_DEBUG': 'false'
    }
    
    print("Setting environment variables:")
    for key, value in test_vars.items():
        os.environ[key] = value
        print(f"  {key}={value}")
    
    # Read variables
    print("\nReading variables:")
    for key in test_vars:
        value = os.getenv(key, 'Not set')
        print(f"  {key}={value}")
    
    # Clean up
    for key in test_vars:
        os.environ.pop(key, None)
    
    print()

# ============================================================
# CHALLENGE 5: Process Runner
# ============================================================

def process_runner():
    """
    Run external commands safely.
    """
    print("--- Challenge 5: Process Runner ---")
    
    # Run simple command
    try:
        result = subprocess.run(
            ['python', '--version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        print(f"Command: python --version")
        print(f"Return code: {result.returncode}")
        print(f"Output: {result.stdout.strip()}")
        
        if result.returncode == 0:
            print("Status: ✓ Success")
        else:
            print("Status: ✗ Failed")
    
    except subprocess.TimeoutExpired:
        print("Status: ✗ Timeout")
    except FileNotFoundError:
        print("Status: ✗ Command not found")
    
    print()

# ============================================================
# CHALLENGE 6: Timestamp Formatter
# ============================================================

def timestamp_formatter():
    """
    Format timestamps in various ways.
    """
    print("--- Challenge 6: Timestamp Formatter ---")
    
    now = datetime.now()
    
    formats = [
        ("%Y-%m-%d", "ISO Date"),
        ("%Y-%m-%d %H:%M:%S", "ISO DateTime"),
        ("%B %d, %Y", "Long Date"),
        ("%I:%M %p", "12-hour Time"),
        ("%A, %B %d, %Y", "Full Date"),
    ]
    
    print(f"Current time: {now}")
    print("\nFormatted:")
    for fmt, description in formats:
        formatted = now.strftime(fmt)
        print(f"  {description:20} {formatted}")
    
    print()

# ============================================================
# CHALLENGE 7: Complete System Tool
# ============================================================

def complete_system_tool():
    """
    Build complete system utility.
    """
    print("--- Challenge 7: Complete System Tool ---")
    
    print("=" * 60)
    print("SYSTEM UTILITY")
    print("=" * 60)
    
    # System info
    print("\n[System]")
    print(f"Platform: {sys.platform}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"PID: {os.getpid()}")
    
    # Directory info
    print("\n[Current Directory]")
    cwd = Path.cwd()
    print(f"Path: {cwd}")
    
    try:
        items = list(cwd.iterdir())
        print(f"Items: {len(items)}")
    except PermissionError:
        print("Items: Permission denied")
    
    # Time info
    print("\n[Time]")
    now = datetime.now()
    print(f"Current: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """Self-assessment checklist for Week 10"""
    print("=" * 60)
    print("WEEK 10 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("os module", "Can you work with environment and file system?"),
        ("sys module", "Can you access system parameters?"),
        ("subprocess", "Can you run external commands?"),
        ("shutil", "Can you perform file operations?"),
        ("datetime", "Can you work with dates and times?"),
        ("platform", "Can you write cross-platform code?"),
        ("System tools", "Can you build system utilities?"),
    ]
    
    print("\nRate yourself (1-5) on these concepts:\n")
    for i, (topic, question) in enumerate(checklist, 1):
        print(f"{i}. {topic}")
        print(f"   {question}")
        print()
    
    print("=" * 60)
    print()

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 10, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week10_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    system_info_tool()
    file_backup_utility()
    directory_statistics()
    environment_manager()
    process_runner()
    timestamp_formatter()
    complete_system_tool()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 10 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered system programming!")
    print("\n📚 Next: Week 11 - Concurrency")
    print("\n💡 Build powerful system tools with Python!")

