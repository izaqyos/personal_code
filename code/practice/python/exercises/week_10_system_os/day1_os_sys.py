"""
Week 10, Day 1: os and sys Modules

Learning Objectives:
- Master os module for OS interface
- Learn sys module for system parameters
- Practice environment variables
- Handle process information
- Build system utilities

Time: 10-15 minutes
"""

import os
import sys
from pathlib import Path

# ============================================================
# EXERCISE 1: Environment Variables
# ============================================================

def environment_variables():
    """
    Work with environment variables.
    
    Environment: System-wide configuration
    """
    print("--- Exercise 1: Environment Variables ---")
    
    # Get environment variable
    home = os.getenv('HOME') or os.getenv('USERPROFILE')
    print(f"Home directory: {home}")
    
    # Get with default
    api_key = os.getenv('API_KEY', 'default_key')
    print(f"API key: {api_key}")
    
    # Set environment variable
    os.environ['MY_VAR'] = 'my_value'
    print(f"MY_VAR: {os.environ['MY_VAR']}")
    
    # List all environment variables
    print(f"\nTotal environment variables: {len(os.environ)}")
    
    # Common variables
    common_vars = ['PATH', 'HOME', 'USER', 'SHELL']
    print("\nCommon variables:")
    for var in common_vars:
        value = os.getenv(var, 'Not set')
        print(f"  {var}: {value[:50] if len(value) > 50 else value}")
    
    print()

# ============================================================
# EXERCISE 2: System Information
# ============================================================

def system_information():
    """
    Get system information.
    
    TODO: Platform, version, paths
    """
    print("--- Exercise 2: System Information ---")
    
    # Python information
    print("Python:")
    print(f"  Version: {sys.version}")
    print(f"  Executable: {sys.executable}")
    print(f"  Platform: {sys.platform}")
    
    # System paths
    print(f"\nPython path ({len(sys.path)} entries):")
    for i, path in enumerate(sys.path[:3], 1):
        print(f"  {i}. {path}")
    
    # Current working directory
    print(f"\nCurrent directory: {os.getcwd()}")
    
    # Process ID
    print(f"Process ID: {os.getpid()}")
    
    # User information
    if hasattr(os, 'getuid'):
        print(f"User ID: {os.getuid()}")
    
    print()

# ============================================================
# EXERCISE 3: Command-Line Arguments
# ============================================================

def command_line_arguments():
    """
    Access command-line arguments.
    
    TODO: sys.argv
    """
    print("--- Exercise 3: Command-Line Arguments ---")
    
    print(f"Script name: {sys.argv[0]}")
    print(f"Arguments: {sys.argv[1:]}")
    print(f"Total arguments: {len(sys.argv) - 1}")
    
    # Simulate processing arguments
    if len(sys.argv) > 1:
        print("\nProcessing arguments:")
        for i, arg in enumerate(sys.argv[1:], 1):
            print(f"  Arg {i}: {arg}")
    else:
        print("\nNo arguments provided")
        print("Usage: python script.py arg1 arg2 ...")
    
    print()

# ============================================================
# EXERCISE 4: Exit Codes
# ============================================================

def exit_codes():
    """
    Understand exit codes.
    
    TODO: sys.exit(), exit codes
    """
    print("--- Exercise 4: Exit Codes ---")
    
    print("Exit codes:")
    print("  0: Success")
    print("  1: General error")
    print("  2: Misuse of shell command")
    print("  126: Command cannot execute")
    print("  127: Command not found")
    print("  128+n: Fatal error signal n")
    
    print("\nUsage:")
    print("  sys.exit(0)  # Success")
    print("  sys.exit(1)  # Error")
    print("  sys.exit('Error message')  # Prints message and exits with 1")
    
    print("\n💡 Always return appropriate exit codes")
    print("💡 0 = success, non-zero = error")
    
    print()

# ============================================================
# EXERCISE 5: File System Operations
# ============================================================

def filesystem_operations():
    """
    Basic file system operations.
    
    TODO: os.path, os.listdir, os.walk
    """
    print("--- Exercise 5: File System Operations ---")
    
    # Current directory contents
    cwd = os.getcwd()
    print(f"Current directory: {cwd}")
    
    try:
        items = os.listdir('.')
        print(f"Items in current directory: {len(items)}")
        
        # Separate files and directories
        files = [item for item in items if os.path.isfile(item)]
        dirs = [item for item in items if os.path.isdir(item)]
        
        print(f"  Files: {len(files)}")
        print(f"  Directories: {len(dirs)}")
        
        # Show first few items
        print("\nFirst few items:")
        for item in items[:5]:
            item_type = "DIR" if os.path.isdir(item) else "FILE"
            print(f"  [{item_type}] {item}")
    
    except PermissionError:
        print("Permission denied")
    
    print()

# ============================================================
# EXERCISE 6: Path Manipulation
# ============================================================

def path_manipulation():
    """
    Manipulate file paths.
    
    TODO: os.path operations
    """
    print("--- Exercise 6: Path Manipulation ---")
    
    # Path operations
    path = "/home/user/documents/file.txt"
    
    print(f"Path: {path}")
    print(f"  dirname: {os.path.dirname(path)}")
    print(f"  basename: {os.path.basename(path)}")
    print(f"  split: {os.path.split(path)}")
    print(f"  splitext: {os.path.splitext(path)}")
    
    # Join paths
    joined = os.path.join("home", "user", "documents", "file.txt")
    print(f"\nJoined: {joined}")
    
    # Absolute path
    abs_path = os.path.abspath(".")
    print(f"Absolute path of '.': {abs_path}")
    
    # Path existence
    print(f"\nPath exists: {os.path.exists('.')}")
    print(f"Is file: {os.path.isfile('.')}")
    print(f"Is directory: {os.path.isdir('.')}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World - System Info Tool
# ============================================================

def system_info_tool():
    """
    Build system information tool.
    
    TODO: Comprehensive system info
    """
    print("--- Exercise 7: System Info Tool ---")
    
    print("=" * 60)
    print("SYSTEM INFORMATION")
    print("=" * 60)
    
    # Python
    print("\nPython:")
    print(f"  Version: {sys.version.split()[0]}")
    print(f"  Implementation: {sys.implementation.name}")
    print(f"  Executable: {sys.executable}")
    
    # Platform
    print(f"\nPlatform:")
    print(f"  System: {sys.platform}")
    
    # Directories
    print(f"\nDirectories:")
    print(f"  Current: {os.getcwd()}")
    print(f"  Home: {os.getenv('HOME') or os.getenv('USERPROFILE')}")
    
    # Process
    print(f"\nProcess:")
    print(f"  PID: {os.getpid()}")
    
    # Environment
    print(f"\nEnvironment:")
    print(f"  Variables: {len(os.environ)}")
    
    print("\n" + "=" * 60)
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    os and sys Complexity:
    
    Time Complexity:
    - os.getenv(): O(1)
    - os.listdir(): O(n) where n is items
    - os.walk(): O(n) for all files/dirs
    - sys.exit(): O(1)
    
    Best Practices:
    - Use os.getenv() with defaults
    - Check os.path.exists() before operations
    - Use pathlib for modern code
    - Handle PermissionError
    - Return appropriate exit codes
    
    Security:
    - Validate environment variables
    - Sanitize file paths
    - Check permissions
    - Avoid shell injection
    - Limit file system access
    
    Cross-Platform:
    - Use os.path.join() for paths
    - Check sys.platform for OS-specific code
    - Use pathlib for modern code
    - Test on target platforms
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 10, Day 1: os and sys Modules")
    print("=" * 60)
    print()
    
    environment_variables()
    system_information()
    command_line_arguments()
    exit_codes()
    filesystem_operations()
    path_manipulation()
    system_info_tool()
    
    print("=" * 60)
    print("✅ Day 1 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. os: Operating system interface")
    print("2. sys: System-specific parameters")
    print("3. Environment variables for configuration")
    print("4. Exit codes for error handling")

