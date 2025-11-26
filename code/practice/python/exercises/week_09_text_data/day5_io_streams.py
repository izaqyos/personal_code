"""
Week 9, Day 5: I/O and Streams

Learning Objectives:
- Master StringIO and BytesIO
- Learn file modes and buffering
- Practice stream operations
- Handle binary data
- Build I/O utilities

Time: 10-15 minutes
"""

import io
import sys
from contextlib import redirect_stdout, redirect_stderr

# ============================================================
# EXERCISE 1: StringIO Basics
# ============================================================

def stringio_basics():
    """
    Learn in-memory text streams.
    
    StringIO: Text stream in memory
    """
    print("--- Exercise 1: StringIO Basics ---")
    
    # Create StringIO
    stream = io.StringIO()
    
    # Write to stream
    stream.write("Hello, ")
    stream.write("World!\n")
    print(f"Position after write: {stream.tell()}")
    
    # Get value
    content = stream.getvalue()
    print(f"Content: {repr(content)}")
    
    # Seek and read
    stream.seek(0)
    line = stream.readline()
    print(f"First line: {repr(line)}")
    
    # Initialize with content
    stream2 = io.StringIO("Initial\nContent\nHere")
    print(f"\nInitialized stream:")
    for line in stream2:
        print(f"  {line.rstrip()}")
    
    print()

# ============================================================
# EXERCISE 2: BytesIO for Binary Data
# ============================================================

def bytesio_basics():
    """
    Learn in-memory binary streams.
    
    TODO: BytesIO for bytes
    """
    print("--- Exercise 2: BytesIO for Binary Data ---")
    
    # Create BytesIO
    stream = io.BytesIO()
    
    # Write bytes
    stream.write(b"Hello, ")
    stream.write(b"Binary!\n")
    
    # Get value
    content = stream.getvalue()
    print(f"Content: {content}")
    print(f"Hex: {content.hex()}")
    
    # Seek and read
    stream.seek(0)
    chunk = stream.read(5)
    print(f"First 5 bytes: {chunk}")
    
    # Initialize with bytes
    stream2 = io.BytesIO(b"\x00\x01\x02\x03\x04")
    print(f"\nInitialized stream:")
    stream2.seek(0)
    while True:
        byte = stream2.read(1)
        if not byte:
            break
        print(f"  Byte: 0x{byte.hex()}")
    
    print()

# ============================================================
# EXERCISE 3: Stream Operations
# ============================================================

def stream_operations():
    """
    Master stream positioning and reading.
    
    TODO: seek, tell, read, readline
    """
    print("--- Exercise 3: Stream Operations ---")
    
    content = "Line 1\nLine 2\nLine 3\nLine 4"
    stream = io.StringIO(content)
    
    # Read all
    print("read():")
    print(f"  {repr(stream.read())}")
    
    # Reset and read lines
    stream.seek(0)
    print("\nreadline():")
    print(f"  {repr(stream.readline())}")
    print(f"  {repr(stream.readline())}")
    
    # Reset and read all lines
    stream.seek(0)
    print("\nreadlines():")
    lines = stream.readlines()
    for i, line in enumerate(lines, 1):
        print(f"  {i}: {repr(line)}")
    
    # Seek operations
    stream.seek(0)
    print(f"\nPosition at start: {stream.tell()}")
    stream.read(5)
    print(f"Position after read(5): {stream.tell()}")
    stream.seek(0, io.SEEK_END)
    print(f"Position at end: {stream.tell()}")
    
    print()

# ============================================================
# EXERCISE 4: Redirecting Output
# ============================================================

def redirecting_output():
    """
    Redirect stdout and stderr.
    
    TODO: Capture print output
    """
    print("--- Exercise 4: Redirecting Output ---")
    
    # Capture stdout
    captured = io.StringIO()
    
    with redirect_stdout(captured):
        print("This goes to StringIO")
        print("Not to console")
    
    print("Back to console")
    print(f"Captured: {repr(captured.getvalue())}")
    
    # Capture stderr
    captured_err = io.StringIO()
    
    with redirect_stderr(captured_err):
        print("Error message", file=sys.stderr)
    
    print(f"Captured error: {repr(captured_err.getvalue())}")
    
    print()

# ============================================================
# EXERCISE 5: File Modes and Buffering
# ============================================================

def file_modes():
    """
    Understand file modes.
    
    TODO: r, w, a, b, +, buffering
    """
    print("--- Exercise 5: File Modes ---")
    
    print("Common file modes:")
    modes = [
        ("'r'", "Read (default)"),
        ("'w'", "Write (truncate)"),
        ("'a'", "Append"),
        ("'x'", "Exclusive create"),
        ("'r+'", "Read and write"),
        ("'rb'", "Read binary"),
        ("'wb'", "Write binary"),
        ("'ab'", "Append binary"),
    ]
    
    for mode, description in modes:
        print(f"  {mode:6} - {description}")
    
    print("\nBuffering:")
    print("  0  - Unbuffered (binary only)")
    print("  1  - Line buffered (text only)")
    print("  >1 - Buffer size in bytes")
    print("  -1 - System default")
    
    print()

# ============================================================
# EXERCISE 6: Text vs Binary Mode
# ============================================================

def text_vs_binary():
    """
    Understand text vs binary mode.
    
    TODO: Encoding, newlines
    """
    print("--- Exercise 6: Text vs Binary Mode ---")
    
    text = "Hello, 世界!\n"
    
    # Text mode (automatic encoding)
    text_stream = io.StringIO(text)
    print(f"Text mode: {repr(text_stream.getvalue())}")
    
    # Binary mode (explicit encoding)
    binary_stream = io.BytesIO(text.encode('utf-8'))
    print(f"Binary mode: {binary_stream.getvalue()}")
    print(f"Hex: {binary_stream.getvalue().hex()}")
    
    # Decode back
    binary_stream.seek(0)
    decoded = binary_stream.read().decode('utf-8')
    print(f"Decoded: {repr(decoded)}")
    
    print("\n💡 Text mode:")
    print("  • Automatic encoding/decoding")
    print("  • Newline translation")
    print("  • Works with str")
    
    print("\n💡 Binary mode:")
    print("  • No encoding (raw bytes)")
    print("  • No newline translation")
    print("  • Works with bytes")
    
    print()

# ============================================================
# EXERCISE 7: Real-World - CSV to JSON Converter
# ============================================================

def csv_to_json_converter():
    """
    Convert CSV to JSON using streams.
    
    TODO: Stream processing
    """
    print("--- Exercise 7: CSV to JSON Converter ---")
    
    import csv
    import json
    
    # Input CSV
    csv_data = """name,age,city
Alice,30,NYC
Bob,25,LA
Carol,28,Chicago"""
    
    # Parse CSV
    csv_stream = io.StringIO(csv_data)
    reader = csv.DictReader(csv_stream)
    records = list(reader)
    
    # Convert to JSON
    json_stream = io.StringIO()
    json.dump(records, json_stream, indent=2)
    
    # Output
    json_stream.seek(0)
    json_output = json_stream.read()
    
    print("Input CSV:")
    print(csv_data)
    print("\nOutput JSON:")
    print(json_output)
    
    print()

# ============================================================
# STREAM UTILITIES
# ============================================================

def stream_utilities():
    """
    Useful stream utilities.
    """
    print("--- Stream Utilities ---")
    
    def copy_stream(source, dest, chunk_size=1024):
        """Copy data from source to dest stream"""
        while True:
            chunk = source.read(chunk_size)
            if not chunk:
                break
            dest.write(chunk)
    
    # Example usage
    source = io.StringIO("A" * 5000)
    dest = io.StringIO()
    
    copy_stream(source, dest, chunk_size=1000)
    print(f"Copied {len(dest.getvalue())} characters")
    
    # Peek without consuming
    def peek_stream(stream, n=10):
        """Peek at stream without changing position"""
        pos = stream.tell()
        data = stream.read(n)
        stream.seek(pos)
        return data
    
    stream = io.StringIO("Hello, World!")
    peeked = peek_stream(stream, 5)
    print(f"Peeked: {repr(peeked)}")
    print(f"Position unchanged: {stream.tell()}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    I/O and Streams Complexity:
    
    Time Complexity:
    - StringIO/BytesIO creation: O(1)
    - write: O(n) where n is data size
    - read: O(n)
    - seek: O(1)
    - tell: O(1)
    
    Space Complexity:
    - StringIO: O(n) for stored data
    - BytesIO: O(n) for stored bytes
    - Buffer: O(k) where k is buffer size
    
    Best Practices:
    - Use StringIO for text in memory
    - Use BytesIO for binary in memory
    - Close streams when done
    - Use context managers
    - Choose appropriate buffer size
    
    Performance:
    - StringIO faster than file I/O
    - Buffering improves performance
    - Seek is fast (in-memory)
    - Read/write in chunks
    
    Security:
    - Validate data before writing
    - Limit stream size
    - Handle encoding errors
    - Clean up sensitive data
    
    When to Use:
    - StringIO: Testing, string building
    - BytesIO: Binary data, protocols
    - Files: Persistent storage
    - Sockets: Network I/O
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 9, Day 5: I/O and Streams")
    print("=" * 60)
    print()
    
    stringio_basics()
    bytesio_basics()
    stream_operations()
    redirecting_output()
    file_modes()
    text_vs_binary()
    csv_to_json_converter()
    stream_utilities()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. StringIO: In-memory text streams")
    print("2. BytesIO: In-memory binary streams")
    print("3. Use for testing and string building")
    print("4. Understand text vs binary mode")

