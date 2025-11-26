"""
Week 9, Day 3: JSON and CSV Processing

Learning Objectives:
- Master JSON encoding/decoding
- Learn CSV reading/writing
- Practice data serialization
- Handle structured data
- Build data pipelines

Time: 10-15 minutes
"""

import json
import csv
import io
from typing import List, Dict, Any
from datetime import datetime
from decimal import Decimal

# ============================================================
# EXERCISE 1: JSON Basics
# ============================================================

def json_basics():
    """
    Learn JSON encoding and decoding.
    
    JSON: JavaScript Object Notation
    """
    print("--- Exercise 1: JSON Basics ---")
    
    # Python to JSON
    data = {
        "name": "Alice",
        "age": 30,
        "active": True,
        "scores": [95, 87, 92],
        "address": {"city": "NYC", "zip": "10001"}
    }
    
    json_str = json.dumps(data)
    print("Python to JSON:")
    print(json_str)
    
    # Pretty printing
    json_pretty = json.dumps(data, indent=2)
    print("\nPretty JSON:")
    print(json_pretty)
    
    # JSON to Python
    parsed = json.loads(json_str)
    print("\nJSON to Python:")
    print(f"Name: {parsed['name']}, Age: {parsed['age']}")
    
    print()

# ============================================================
# EXERCISE 2: JSON Files
# ============================================================

def json_files():
    """
    Read and write JSON files.
    
    TODO: File I/O with JSON
    """
    print("--- Exercise 2: JSON Files ---")
    
    # Write to file
    data = {
        "users": [
            {"id": 1, "name": "Bob", "email": "bob@example.com"},
            {"id": 2, "name": "Carol", "email": "carol@example.com"}
        ],
        "timestamp": datetime.now().isoformat()
    }
    
    # Simulate file with StringIO
    file_content = io.StringIO()
    json.dump(data, file_content, indent=2)
    
    print("Written to file:")
    print(file_content.getvalue())
    
    # Read from file
    file_content.seek(0)
    loaded = json.load(file_content)
    
    print("\nRead from file:")
    print(f"Users: {len(loaded['users'])}")
    for user in loaded['users']:
        print(f"  {user['name']}: {user['email']}")
    
    print()

# ============================================================
# EXERCISE 3: Custom JSON Encoding
# ============================================================

def custom_json_encoding():
    """
    Handle non-serializable objects.
    
    TODO: Custom JSONEncoder
    """
    print("--- Exercise 3: Custom JSON Encoding ---")
    
    class DateTimeEncoder(json.JSONEncoder):
        """Custom encoder for datetime objects"""
        def default(self, obj):
            if isinstance(obj, datetime):
                return obj.isoformat()
            if isinstance(obj, Decimal):
                return float(obj)
            return super().default(obj)
    
    data = {
        "event": "Meeting",
        "date": datetime.now(),
        "cost": Decimal("99.99")
    }
    
    # This would fail with default encoder
    # json.dumps(data)  # TypeError
    
    # Use custom encoder
    json_str = json.dumps(data, cls=DateTimeEncoder, indent=2)
    print("Custom encoded:")
    print(json_str)
    
    # Alternative: default function
    def json_serial(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError(f"Type {type(obj)} not serializable")
    
    json_str2 = json.dumps(data, default=json_serial, indent=2)
    print("\nWith default function:")
    print(json_str2)
    
    print()

# ============================================================
# EXERCISE 4: CSV Reading
# ============================================================

def csv_reading():
    """
    Read CSV files.
    
    TODO: csv.reader and csv.DictReader
    """
    print("--- Exercise 4: CSV Reading ---")
    
    # Sample CSV data
    csv_data = """name,age,city
Alice,30,NYC
Bob,25,LA
Carol,28,Chicago"""
    
    # Using csv.reader
    print("csv.reader:")
    file = io.StringIO(csv_data)
    reader = csv.reader(file)
    
    for row in reader:
        print(f"  {row}")
    
    # Using csv.DictReader
    print("\ncsv.DictReader:")
    file = io.StringIO(csv_data)
    reader = csv.DictReader(file)
    
    for row in reader:
        print(f"  {row['name']}: {row['age']} years, {row['city']}")
    
    print()

# ============================================================
# EXERCISE 5: CSV Writing
# ============================================================

def csv_writing():
    """
    Write CSV files.
    
    TODO: csv.writer and csv.DictWriter
    """
    print("--- Exercise 5: CSV Writing ---")
    
    # Using csv.writer
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Name', 'Age', 'Score'])
    writer.writerow(['Dave', 32, 95])
    writer.writerow(['Eve', 27, 88])
    
    print("csv.writer output:")
    print(output.getvalue())
    
    # Using csv.DictWriter
    output2 = io.StringIO()
    fieldnames = ['name', 'age', 'score']
    writer2 = csv.DictWriter(output2, fieldnames=fieldnames)
    
    writer2.writeheader()
    writer2.writerow({'name': 'Frank', 'age': 29, 'score': 92})
    writer2.writerow({'name': 'Grace', 'age': 31, 'score': 87})
    
    print("csv.DictWriter output:")
    print(output2.getvalue())
    
    print()

# ============================================================
# EXERCISE 6: CSV Dialects and Options
# ============================================================

def csv_dialects():
    """
    Handle different CSV formats.
    
    TODO: Delimiters, quotes, escaping
    """
    print("--- Exercise 6: CSV Dialects ---")
    
    # Custom delimiter
    data = [['Name', 'Score'], ['Alice', '95'], ['Bob', '87']]
    
    # Tab-separated
    output_tsv = io.StringIO()
    writer = csv.writer(output_tsv, delimiter='\t')
    writer.writerows(data)
    
    print("Tab-separated:")
    print(output_tsv.getvalue())
    
    # Pipe-separated
    output_pipe = io.StringIO()
    writer = csv.writer(output_pipe, delimiter='|')
    writer.writerows(data)
    
    print("Pipe-separated:")
    print(output_pipe.getvalue())
    
    # Handle quotes
    data_quotes = [['Name', 'Comment'], ['Alice', 'Said "Hello"']]
    output_quotes = io.StringIO()
    writer = csv.writer(output_quotes, quoting=csv.QUOTE_ALL)
    writer.writerows(data_quotes)
    
    print("With quotes:")
    print(output_quotes.getvalue())
    
    print()

# ============================================================
# EXERCISE 7: Real-World - Data Pipeline
# ============================================================

def data_pipeline():
    """
    Convert between JSON and CSV.
    
    TODO: Transform data formats
    """
    print("--- Exercise 7: Data Pipeline ---")
    
    # JSON data
    json_data = {
        "employees": [
            {"id": 1, "name": "Helen", "dept": "Engineering", "salary": 90000},
            {"id": 2, "name": "Ian", "dept": "Marketing", "salary": 75000},
            {"id": 3, "name": "Jane", "dept": "Sales", "salary": 80000}
        ]
    }
    
    print("Original JSON:")
    print(json.dumps(json_data, indent=2))
    
    # Convert to CSV
    print("\nConverted to CSV:")
    output = io.StringIO()
    
    employees = json_data['employees']
    if employees:
        fieldnames = employees[0].keys()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(employees)
    
    csv_content = output.getvalue()
    print(csv_content)
    
    # Convert back to JSON
    print("Converted back to JSON:")
    input_csv = io.StringIO(csv_content)
    reader = csv.DictReader(input_csv)
    
    employees_back = list(reader)
    json_back = {"employees": employees_back}
    
    print(json.dumps(json_back, indent=2))
    
    print()

# ============================================================
# DATA VALIDATION
# ============================================================

def data_validation():
    """
    Validate JSON and CSV data.
    """
    print("--- Data Validation ---")
    
    # JSON schema validation (conceptual)
    def validate_user(data):
        """Validate user data"""
        required = ['name', 'email', 'age']
        
        for field in required:
            if field not in data:
                return False, f"Missing field: {field}"
        
        if not isinstance(data['age'], int) or data['age'] < 0:
            return False, "Invalid age"
        
        if '@' not in data['email']:
            return False, "Invalid email"
        
        return True, "Valid"
    
    test_cases = [
        {"name": "Alice", "email": "alice@example.com", "age": 30},
        {"name": "Bob", "email": "invalid", "age": 25},
        {"name": "Carol", "age": 28},
    ]
    
    for data in test_cases:
        valid, message = validate_user(data)
        status = "✓" if valid else "✗"
        print(f"{status} {data}: {message}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    JSON/CSV Complexity:
    
    JSON:
    - Encoding: O(n) where n is data size
    - Decoding: O(n)
    - Space: O(n) for parsed data
    - Nested structures supported
    
    CSV:
    - Reading: O(n) where n is file size
    - Writing: O(n)
    - Space: O(1) per row (streaming)
    - Flat structure only
    
    Best Practices:
    - Use json.load/dump for files
    - Use json.loads/dumps for strings
    - Stream large CSV files
    - Validate data after parsing
    - Handle encoding (UTF-8)
    
    Security:
    - Validate JSON structure
    - Limit JSON depth/size
    - Sanitize CSV input
    - Avoid eval() on JSON
    - Check for injection in CSV
    
    Performance:
    - JSON faster for nested data
    - CSV better for tabular data
    - Consider compression
    - Use generators for large files
    
    When to Use:
    - JSON: APIs, config, nested data
    - CSV: Spreadsheets, tabular data
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 9, Day 3: JSON and CSV Processing")
    print("=" * 60)
    print()
    
    json_basics()
    json_files()
    custom_json_encoding()
    csv_reading()
    csv_writing()
    csv_dialects()
    data_pipeline()
    data_validation()
    
    print("=" * 60)
    print("✅ Day 3 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. JSON: Nested, API-friendly")
    print("2. CSV: Tabular, spreadsheet-friendly")
    print("3. Validate data after parsing")
    print("4. Stream large files")

