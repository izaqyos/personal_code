"""
Week 9, Day 7: Review & Challenge - Text & Data Processing

Learning Objectives:
- Review all Week 9 concepts
- Apply text processing techniques
- Practice data manipulation
- Build complete applications
- Master standard library tools

Challenge: Build practical text/data tools

Time: 15-20 minutes
"""

import re
import json
import csv
from pathlib import Path
from io import StringIO
import argparse
import logging

# ============================================================
# REVIEW: Week 9 Concepts
# ============================================================

def week9_review():
    """Quick review of all Week 9 concepts"""
    print("=" * 60)
    print("WEEK 9 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Regular Expressions")
    print("  • Pattern matching with re")
    print("  • Groups and capturing")
    print("  • Substitution and splitting")
    
    print("\nDay 2: String Formatting")
    print("  • F-strings (fast, readable)")
    print("  • format() method")
    print("  • string.Template (safe)")
    
    print("\nDay 3: JSON and CSV")
    print("  • JSON: Nested, API-friendly")
    print("  • CSV: Tabular, spreadsheet")
    print("  • Data serialization")
    
    print("\nDay 4: pathlib")
    print("  • Object-oriented paths")
    print("  • Cross-platform")
    print("  • Path operations")
    
    print("\nDay 5: I/O and Streams")
    print("  • StringIO, BytesIO")
    print("  • Stream operations")
    print("  • Text vs binary mode")
    
    print("\nDay 6: Argparse & Logging")
    print("  • CLI argument parsing")
    print("  • Professional logging")
    print("  • Configuration")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Log Analyzer
# ============================================================

def log_analyzer():
    """
    Analyze log files with regex.
    
    TODO: Parse, filter, summarize logs
    """
    print("--- Challenge 1: Log Analyzer ---")
    
    # Sample log data
    log_data = """2024-03-15 10:30:45 INFO User login: alice@example.com
2024-03-15 10:31:12 ERROR Database connection failed: timeout
2024-03-15 10:32:05 WARNING High memory usage: 85%
2024-03-15 10:33:20 ERROR API timeout: /api/users
2024-03-15 10:34:15 INFO User logout: bob@example.com
2024-03-15 10:35:30 ERROR File not found: /data/file.txt
2024-03-15 10:36:45 INFO User login: carol@example.com"""
    
    # Parse logs
    pattern = r'(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (\w+) (.+)'
    
    logs = []
    for line in log_data.strip().split('\n'):
        match = re.match(pattern, line)
        if match:
            date, time, level, message = match.groups()
            logs.append({
                'date': date,
                'time': time,
                'level': level,
                'message': message
            })
    
    # Analyze
    print(f"Total logs: {len(logs)}")
    
    # Count by level
    from collections import Counter
    level_counts = Counter(log['level'] for log in logs)
    print(f"\nBy level:")
    for level, count in level_counts.most_common():
        print(f"  {level}: {count}")
    
    # Find errors
    errors = [log for log in logs if log['level'] == 'ERROR']
    print(f"\nErrors ({len(errors)}):")
    for error in errors:
        print(f"  {error['time']}: {error['message']}")
    
    print()

# ============================================================
# CHALLENGE 2: Data Format Converter
# ============================================================

def data_format_converter():
    """
    Convert between JSON, CSV, and formatted text.
    
    TODO: Multi-format conversion
    """
    print("--- Challenge 2: Data Format Converter ---")
    
    # Original data
    data = [
        {"name": "Alice", "age": 30, "city": "NYC", "score": 95.5},
        {"name": "Bob", "age": 25, "city": "LA", "score": 87.3},
        {"name": "Carol", "age": 28, "city": "Chicago", "score": 92.1}
    ]
    
    print("Original data (Python):")
    for item in data:
        print(f"  {item}")
    
    # To JSON
    json_output = json.dumps(data, indent=2)
    print("\nJSON format:")
    print(json_output)
    
    # To CSV
    csv_output = StringIO()
    if data:
        writer = csv.DictWriter(csv_output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    print("\nCSV format:")
    print(csv_output.getvalue())
    
    # To formatted table
    print("Table format:")
    print(f"{'Name':<10} {'Age':>5} {'City':<10} {'Score':>7}")
    print("-" * 35)
    for item in data:
        print(f"{item['name']:<10} {item['age']:>5} {item['city']:<10} {item['score']:>7.1f}")
    
    print()

# ============================================================
# CHALLENGE 3: File Processor CLI
# ============================================================

def file_processor_cli():
    """
    Build CLI tool for file processing.
    
    TODO: Complete CLI with logging
    """
    print("--- Challenge 3: File Processor CLI ---")
    
    def process_file(input_path, output_path, operation, verbose):
        """Process file with specified operation"""
        # Configure logging
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format='%(levelname)s: %(message)s'
        )
        logger = logging.getLogger('processor')
        
        logger.info(f"Processing: {input_path}")
        logger.debug(f"Operation: {operation}")
        logger.debug(f"Output: {output_path}")
        
        # Simulate processing
        if operation == 'uppercase':
            logger.info("Converting to uppercase")
            result = "PROCESSED CONTENT"
        elif operation == 'count':
            logger.info("Counting words")
            result = "Word count: 42"
        else:
            logger.warning(f"Unknown operation: {operation}")
            result = "No operation performed"
        
        logger.info("Processing complete")
        return result
    
    # Create parser
    parser = argparse.ArgumentParser(
        description='File processor tool',
        epilog='Example: processor input.txt -o output.txt --op uppercase'
    )
    
    parser.add_argument('input', help='Input file path')
    parser.add_argument('-o', '--output', default='output.txt',
                       help='Output file path')
    parser.add_argument('--op', '--operation',
                       choices=['uppercase', 'lowercase', 'count'],
                       default='uppercase',
                       help='Operation to perform')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Verbose output')
    
    # Test
    test_args = ['input.txt', '-o', 'result.txt', '--op', 'uppercase', '-v']
    args = parser.parse_args(test_args)
    
    print(f"Arguments parsed:")
    print(f"  Input: {args.input}")
    print(f"  Output: {args.output}")
    print(f"  Operation: {args.op}")
    print(f"  Verbose: {args.verbose}")
    print()
    
    result = process_file(args.input, args.output, args.op, args.verbose)
    print(f"\nResult: {result}")
    
    print()

# ============================================================
# CHALLENGE 4: Text Statistics
# ============================================================

def text_statistics():
    """
    Compute statistics on text.
    
    TODO: Word count, frequency, readability
    """
    print("--- Challenge 4: Text Statistics ---")
    
    text = """Python is an amazing programming language.
It is widely used for web development, data science, and automation.
Python's simplicity makes it perfect for beginners.
Many companies use Python for their projects."""
    
    # Basic stats
    lines = text.strip().split('\n')
    words = re.findall(r'\b\w+\b', text.lower())
    
    print(f"Text statistics:")
    print(f"  Lines: {len(lines)}")
    print(f"  Words: {len(words)}")
    print(f"  Characters: {len(text)}")
    print(f"  Unique words: {len(set(words))}")
    
    # Word frequency
    from collections import Counter
    word_freq = Counter(words)
    
    print(f"\nTop 5 words:")
    for word, count in word_freq.most_common(5):
        print(f"  {word}: {count}")
    
    # Average word length
    avg_length = sum(len(word) for word in words) / len(words)
    print(f"\nAverage word length: {avg_length:.1f}")
    
    print()

# ============================================================
# CHALLENGE 5: Configuration File Manager
# ============================================================

def config_file_manager():
    """
    Manage configuration files.
    
    TODO: Read, write, validate config
    """
    print("--- Challenge 5: Configuration File Manager ---")
    
    # Default configuration
    default_config = {
        "app_name": "MyApp",
        "version": "1.0.0",
        "settings": {
            "debug": False,
            "port": 8080,
            "host": "localhost"
        },
        "features": ["auth", "api", "logging"]
    }
    
    # Write config
    config_json = json.dumps(default_config, indent=2)
    print("Configuration (JSON):")
    print(config_json)
    
    # Read and validate
    loaded_config = json.loads(config_json)
    
    def validate_config(config):
        """Validate configuration"""
        required = ["app_name", "version", "settings"]
        for key in required:
            if key not in config:
                return False, f"Missing required key: {key}"
        
        if not isinstance(config["settings"]["port"], int):
            return False, "Port must be integer"
        
        if config["settings"]["port"] < 1 or config["settings"]["port"] > 65535:
            return False, "Port must be 1-65535"
        
        return True, "Valid"
    
    valid, message = validate_config(loaded_config)
    print(f"\nValidation: {message}")
    
    # Update config
    loaded_config["settings"]["debug"] = True
    loaded_config["settings"]["port"] = 9000
    
    print(f"\nUpdated settings:")
    print(f"  debug: {loaded_config['settings']['debug']}")
    print(f"  port: {loaded_config['settings']['port']}")
    
    print()

# ============================================================
# CHALLENGE 6: Path Utilities
# ============================================================

def path_utilities():
    """
    Build path utility functions.
    
    TODO: Find, filter, organize files
    """
    print("--- Challenge 6: Path Utilities ---")
    
    import tempfile
    
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_path = Path(tmpdir)
        
        # Create test structure
        (tmp_path / "docs").mkdir()
        (tmp_path / "images").mkdir()
        (tmp_path / "scripts").mkdir()
        
        files = [
            "docs/readme.txt",
            "docs/guide.md",
            "images/photo1.jpg",
            "images/photo2.png",
            "scripts/script1.py",
            "scripts/script2.py",
            "config.json"
        ]
        
        for file_path in files:
            (tmp_path / file_path).write_text(f"Content of {file_path}")
        
        # Find all Python files
        py_files = list(tmp_path.rglob("*.py"))
        print(f"Python files: {len(py_files)}")
        for f in py_files:
            print(f"  {f.relative_to(tmp_path)}")
        
        # Find all text files
        text_files = list(tmp_path.rglob("*.txt")) + list(tmp_path.rglob("*.md"))
        print(f"\nText files: {len(text_files)}")
        for f in text_files:
            print(f"  {f.relative_to(tmp_path)}")
        
        # Count by extension
        from collections import Counter
        extensions = Counter(f.suffix for f in tmp_path.rglob("*") if f.is_file())
        print(f"\nFiles by extension:")
        for ext, count in extensions.most_common():
            print(f"  {ext or '(no ext)'}: {count}")
    
    print()

# ============================================================
# CHALLENGE 7: Complete Data Pipeline
# ============================================================

def complete_data_pipeline():
    """
    Build end-to-end data pipeline.
    
    TODO: Read CSV, process, output JSON
    """
    print("--- Challenge 7: Complete Data Pipeline ---")
    
    # Input CSV
    csv_input = """name,age,department,salary
Alice,30,Engineering,90000
Bob,25,Marketing,75000
Carol,28,Engineering,85000
Dave,32,Sales,80000"""
    
    print("Input CSV:")
    print(csv_input)
    
    # Parse CSV
    csv_stream = StringIO(csv_input)
    reader = csv.DictReader(csv_stream)
    data = list(reader)
    
    # Process: Convert types, add computed fields
    for record in data:
        record['age'] = int(record['age'])
        record['salary'] = int(record['salary'])
        record['senior'] = record['age'] >= 30
    
    # Aggregate by department
    from collections import defaultdict
    by_dept = defaultdict(list)
    for record in data:
        by_dept[record['department']].append(record)
    
    # Compute statistics
    stats = {}
    for dept, employees in by_dept.items():
        stats[dept] = {
            'count': len(employees),
            'avg_age': sum(e['age'] for e in employees) / len(employees),
            'avg_salary': sum(e['salary'] for e in employees) / len(employees),
            'total_salary': sum(e['salary'] for e in employees)
        }
    
    # Output JSON
    output = {
        'employees': data,
        'statistics': stats
    }
    
    json_output = json.dumps(output, indent=2)
    print("\nOutput JSON:")
    print(json_output)
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """Self-assessment checklist for Week 9"""
    print("=" * 60)
    print("WEEK 9 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Regex", "Can you write and use regex patterns?"),
        ("Formatting", "Can you format strings professionally?"),
        ("JSON/CSV", "Can you work with structured data?"),
        ("pathlib", "Can you manipulate paths effectively?"),
        ("I/O", "Do you understand streams and modes?"),
        ("CLI", "Can you build command-line tools?"),
        ("Logging", "Can you implement proper logging?"),
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
    print("Week 9, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week9_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    log_analyzer()
    data_format_converter()
    file_processor_cli()
    text_statistics()
    config_file_manager()
    path_utilities()
    complete_data_pipeline()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 9 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered text & data processing!")
    print("\n📚 Next: Week 10 - System & OS")
    print("\n💡 These tools are essential for real-world Python!")

