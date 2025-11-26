"""
Week 9, Day 6: Command-Line Arguments & Logging

Learning Objectives:
- Master argparse for CLI
- Learn logging module
- Practice log configuration
- Build command-line tools
- Handle program arguments

Time: 10-15 minutes
"""

import argparse
import logging
import sys
from io import StringIO

# ============================================================
# EXERCISE 1: Argparse Basics
# ============================================================

def argparse_basics():
    """
    Learn basic argument parsing.
    
    argparse: Command-line argument parser
    """
    print("--- Exercise 1: Argparse Basics ---")
    
    # Create parser
    parser = argparse.ArgumentParser(
        description='Example CLI tool',
        epilog='Thanks for using our tool!'
    )
    
    # Add arguments
    parser.add_argument('name', help='Your name')
    parser.add_argument('--age', type=int, help='Your age')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    # Simulate command line
    test_args = ['Alice', '--age', '30', '--verbose']
    args = parser.parse_args(test_args)
    
    print(f"Parsed arguments:")
    print(f"  name: {args.name}")
    print(f"  age: {args.age}")
    print(f"  verbose: {args.verbose}")
    
    print()

# ============================================================
# EXERCISE 2: Argument Types
# ============================================================

def argument_types():
    """
    Learn different argument types.
    
    TODO: Positional, optional, flags
    """
    print("--- Exercise 2: Argument Types ---")
    
    parser = argparse.ArgumentParser()
    
    # Positional (required)
    parser.add_argument('input_file', help='Input file path')
    
    # Optional with default
    parser.add_argument('--output', '-o', default='output.txt',
                       help='Output file (default: output.txt)')
    
    # Integer
    parser.add_argument('--count', '-n', type=int, default=10,
                       help='Number of items')
    
    # Float
    parser.add_argument('--threshold', type=float, default=0.5,
                       help='Threshold value')
    
    # Boolean flag
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    
    # Count occurrences
    parser.add_argument('--verbose', '-v', action='count', default=0,
                       help='Increase verbosity')
    
    # Choices
    parser.add_argument('--format', choices=['json', 'csv', 'xml'],
                       default='json', help='Output format')
    
    # Test
    test_args = ['input.txt', '--count', '5', '-vv', '--format', 'csv']
    args = parser.parse_args(test_args)
    
    print("Parsed:")
    print(f"  input_file: {args.input_file}")
    print(f"  output: {args.output}")
    print(f"  count: {args.count}")
    print(f"  verbose: {args.verbose}")
    print(f"  format: {args.format}")
    
    print()

# ============================================================
# EXERCISE 3: Subcommands
# ============================================================

def subcommands():
    """
    Create CLI with subcommands.
    
    TODO: Like git (add, commit, push)
    """
    print("--- Exercise 3: Subcommands ---")
    
    parser = argparse.ArgumentParser(prog='mytool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add subcommand
    add_parser = subparsers.add_parser('add', help='Add items')
    add_parser.add_argument('items', nargs='+', help='Items to add')
    
    # Remove subcommand
    remove_parser = subparsers.add_parser('remove', help='Remove items')
    remove_parser.add_argument('items', nargs='+', help='Items to remove')
    
    # List subcommand
    list_parser = subparsers.add_parser('list', help='List items')
    list_parser.add_argument('--all', action='store_true', help='List all')
    
    # Test
    test_cases = [
        ['add', 'item1', 'item2'],
        ['remove', 'item1'],
        ['list', '--all']
    ]
    
    for test_args in test_cases:
        args = parser.parse_args(test_args)
        print(f"Command: {args.command}")
        if hasattr(args, 'items'):
            print(f"  Items: {args.items}")
        if hasattr(args, 'all'):
            print(f"  All: {args.all}")
        print()
    
    print()

# ============================================================
# EXERCISE 4: Logging Basics
# ============================================================

def logging_basics():
    """
    Learn basic logging.
    
    Logging: Better than print for production
    """
    print("--- Exercise 4: Logging Basics ---")
    
    # Configure logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger(__name__)
    
    # Log levels
    logger.debug("Debug message (detailed)")
    logger.info("Info message (general)")
    logger.warning("Warning message (caution)")
    logger.error("Error message (problem)")
    logger.critical("Critical message (severe)")
    
    print("\n💡 Log levels (low to high):")
    print("  DEBUG < INFO < WARNING < ERROR < CRITICAL")
    
    print()

# ============================================================
# EXERCISE 5: Log Configuration
# ============================================================

def log_configuration():
    """
    Configure logging in detail.
    
    TODO: Handlers, formatters, filters
    """
    print("--- Exercise 5: Log Configuration ---")
    
    # Create logger
    logger = logging.getLogger('myapp')
    logger.setLevel(logging.DEBUG)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Formatter
    formatter = logging.Formatter(
        '%(levelname)-8s [%(name)s] %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # Add handler
    logger.addHandler(console_handler)
    
    # Log messages
    logger.debug("This won't show (below INFO)")
    logger.info("This will show")
    logger.warning("This will show")
    
    # Clean up
    logger.removeHandler(console_handler)
    
    print()

# ============================================================
# EXERCISE 6: Logging to Files
# ============================================================

def logging_to_files():
    """
    Log to files with rotation.
    
    TODO: FileHandler, RotatingFileHandler
    """
    print("--- Exercise 6: Logging to Files ---")
    
    import tempfile
    from pathlib import Path
    
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = Path(tmpdir) / 'app.log'
        
        # Create logger
        logger = logging.getLogger('fileapp')
        logger.setLevel(logging.DEBUG)
        
        # File handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        
        # Log messages
        logger.info("Application started")
        logger.debug("Debug information")
        logger.warning("Warning message")
        
        # Read log file
        print(f"Log file contents:")
        print(log_file.read_text())
        
        # Clean up
        logger.removeHandler(file_handler)
        file_handler.close()
    
    print()

# ============================================================
# EXERCISE 7: Real-World - CLI Tool with Logging
# ============================================================

def cli_tool_with_logging():
    """
    Build complete CLI tool.
    
    TODO: Combine argparse and logging
    """
    print("--- Exercise 7: CLI Tool with Logging ---")
    
    def process_data(input_file, output_file, verbose):
        """Process data with logging"""
        # Configure logging based on verbosity
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(levelname)s: %(message)s'
        )
        
        logger = logging.getLogger('processor')
        
        logger.info(f"Processing {input_file}")
        logger.debug(f"Output will be written to {output_file}")
        
        # Simulate processing
        logger.info("Reading data...")
        logger.debug("Validating data...")
        logger.info("Processing complete")
        
        return True
    
    # Create parser
    parser = argparse.ArgumentParser(
        description='Data processor tool'
    )
    parser.add_argument('input', help='Input file')
    parser.add_argument('-o', '--output', default='output.txt',
                       help='Output file')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    # Test
    test_args = ['data.csv', '-o', 'result.json', '--verbose']
    args = parser.parse_args(test_args)
    
    print(f"Running: process_data({args.input}, {args.output}, {args.verbose})")
    print()
    
    process_data(args.input, args.output, args.verbose)
    
    print()

# ============================================================
# BEST PRACTICES
# ============================================================

def best_practices():
    """
    Best practices for CLI and logging.
    """
    print("--- Best Practices ---")
    
    print("Argparse:")
    print("  • Provide clear help messages")
    print("  • Use meaningful argument names")
    print("  • Set sensible defaults")
    print("  • Validate input early")
    print("  • Use subcommands for complex CLIs")
    
    print("\nLogging:")
    print("  • Use appropriate log levels")
    print("  • Log to files in production")
    print("  • Include timestamps")
    print("  • Don't log sensitive data")
    print("  • Use structured logging")
    print("  • Rotate log files")
    
    print("\nLog Levels:")
    print("  • DEBUG: Detailed diagnostic info")
    print("  • INFO: General informational messages")
    print("  • WARNING: Warning messages")
    print("  • ERROR: Error messages")
    print("  • CRITICAL: Critical problems")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Argparse & Logging Complexity:
    
    Argparse:
    - Parsing: O(n) where n is arguments
    - Validation: O(1) per argument
    - Space: O(n) for parsed args
    
    Logging:
    - Log call: O(1) + formatting
    - File write: O(m) where m is message size
    - Buffering improves performance
    
    Best Practices:
    - Use argparse over sys.argv
    - Provide good help text
    - Validate arguments early
    - Use logging over print
    - Configure logging once
    - Use appropriate log levels
    
    Security:
    - Validate all user input
    - Sanitize file paths
    - Don't log passwords/secrets
    - Limit log file size
    - Secure log file permissions
    
    Performance:
    - Argparse is fast enough
    - Logging has minimal overhead
    - Use lazy formatting: logger.debug("x=%s", x)
    - Disable debug logs in production
    
    When to Use:
    - argparse: CLI applications
    - logging: All applications
    - print: Only for user output
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 9, Day 6: Command-Line Arguments & Logging")
    print("=" * 60)
    print()
    
    argparse_basics()
    argument_types()
    subcommands()
    logging_basics()
    log_configuration()
    logging_to_files()
    cli_tool_with_logging()
    best_practices()
    
    print("=" * 60)
    print("✅ Day 6 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. argparse: Professional CLI parsing")
    print("2. logging: Better than print")
    print("3. Use appropriate log levels")
    print("4. Combine for robust CLI tools")

