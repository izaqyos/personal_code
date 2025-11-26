"""
Week 2, Day 5: yield from and Generator Delegation

Learning Objectives:
- Understand yield from syntax and purpose
- Learn generator delegation patterns
- Master recursive generators
- Build composable generator functions

Time: 10-15 minutes
"""

from typing import Generator, Iterable, Any

# ============================================================
# EXERCISE 1: yield from Basics
# ============================================================

def yield_from_basics():
    """
    Compare manual iteration vs yield from.
    
    yield from delegates to another generator
    """
    print("--- Exercise 1: yield from Basics ---")
    
    # Manual way - yielding each item
    def manual_chain(iter1, iter2):
        """Chain iterables manually"""
        for item in iter1:
            yield item
        for item in iter2:
            yield item
    
    # Using yield from
    def yield_from_chain(iter1, iter2):
        """Chain iterables using yield from"""
        yield from iter1
        yield from iter2
    
    # Test both
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    
    print("Manual chaining:")
    print(f"  {list(manual_chain(list1, list2))}")
    
    print("\nUsing yield from:")
    print(f"  {list(yield_from_chain(list1, list2))}")
    
    print()

# ============================================================
# EXERCISE 2: Flattening Nested Structures
# ============================================================

def flatten(nested: Iterable) -> Generator:
    """
    Flatten arbitrarily nested iterables.
    
    TODO: Implement recursive flattening with yield from
    """
    for item in nested:
        if isinstance(item, (list, tuple)) and not isinstance(item, (str, bytes)):
            # Recursively flatten
            yield from flatten(item)
        else:
            yield item

def test_flatten():
    """Test the flatten function"""
    print("--- Exercise 2: Flattening Nested Structures ---")
    
    # TODO: Flatten various nested structures
    nested1 = [1, [2, 3], [4, [5, 6]], 7]
    print(f"Input: {nested1}")
    print(f"Flattened: {list(flatten(nested1))}")
    
    nested2 = [[1, 2], [3, [4, [5, [6, 7]]]]]
    print(f"\nInput: {nested2}")
    print(f"Flattened: {list(flatten(nested2))}")
    
    nested3 = [1, [2, [3, [4, [5]]]]]
    print(f"\nInput: {nested3}")
    print(f"Flattened: {list(flatten(nested3))}")
    
    print()

# ============================================================
# EXERCISE 3: Tree Traversal
# ============================================================

class TreeNode:
    """Simple tree node"""
    def __init__(self, value, children=None):
        self.value = value
        self.children = children or []

def traverse_tree(node: TreeNode) -> Generator:
    """
    Traverse tree and yield all values.
    
    TODO: Implement tree traversal with yield from
    """
    # Yield current node
    yield node.value
    
    # Recursively yield from children
    for child in node.children:
        yield from traverse_tree(child)

def test_tree_traversal():
    """Test tree traversal"""
    print("--- Exercise 3: Tree Traversal ---")
    
    # Build a tree
    #       1
    #      /|\
    #     2 3 4
    #    /|   |
    #   5 6   7
    
    tree = TreeNode(1, [
        TreeNode(2, [
            TreeNode(5),
            TreeNode(6)
        ]),
        TreeNode(3),
        TreeNode(4, [
            TreeNode(7)
        ])
    ])
    
    print("Tree traversal (pre-order):")
    for value in traverse_tree(tree):
        print(f"  {value}")
    
    print()

# ============================================================
# EXERCISE 4: Generator Composition
# ============================================================

def read_files(*filenames) -> Generator[str, None, None]:
    """
    Read multiple files using yield from.
    
    TODO: Implement multi-file reader
    """
    for filename in filenames:
        with open(filename, 'r') as f:
            yield from f

def test_multi_file_reader():
    """Test reading multiple files"""
    print("--- Exercise 4: Generator Composition ---")
    
    # Create test files
    with open('file1.txt', 'w') as f:
        f.write("Line 1 from file 1\n")
        f.write("Line 2 from file 1\n")
    
    with open('file2.txt', 'w') as f:
        f.write("Line 1 from file 2\n")
        f.write("Line 2 from file 2\n")
    
    # Read all files
    print("Reading multiple files:")
    for i, line in enumerate(read_files('file1.txt', 'file2.txt'), 1):
        print(f"  {i}: {line.strip()}")
    
    # Cleanup
    import os
    os.remove('file1.txt')
    os.remove('file2.txt')
    
    print()

# ============================================================
# EXERCISE 5: Delegating with Return Values
# ============================================================

def generator_with_return() -> Generator[int, None, str]:
    """
    Generator that returns a value.
    
    yield from can capture the return value
    """
    yield 1
    yield 2
    yield 3
    return "Done!"

def delegating_generator() -> Generator[int, None, None]:
    """
    Delegate to another generator and capture return value.
    
    TODO: Use yield from to capture return value
    """
    print("  Starting delegation...")
    result = yield from generator_with_return()
    print(f"  Captured return value: {result}")
    yield 4
    yield 5

def test_return_values():
    """Test capturing return values"""
    print("--- Exercise 5: Delegating with Return Values ---")
    
    print("Values from delegating generator:")
    for value in delegating_generator():
        print(f"  Yielded: {value}")
    
    print()

# ============================================================
# EXERCISE 6: Building a Parser
# ============================================================

def parse_numbers(text: str) -> Generator[int, None, None]:
    """Parse numbers from text"""
    for word in text.split():
        if word.isdigit():
            yield int(word)

def parse_words(text: str) -> Generator[str, None, None]:
    """Parse words from text"""
    for word in text.split():
        if word.isalpha():
            yield word.lower()

def parse_all(text: str) -> Generator[Any, None, None]:
    """
    Parse all tokens from text.
    
    TODO: Use yield from to combine parsers
    """
    # First yield all numbers
    yield from parse_numbers(text)
    
    # Then yield all words
    yield from parse_words(text)

def test_parser():
    """Test the parser"""
    print("--- Exercise 6: Building a Parser ---")
    
    text = "There are 42 apples and 17 oranges in the basket"
    
    print(f"Text: {text}")
    print("\nParsed tokens:")
    for token in parse_all(text):
        print(f"  {token} ({type(token).__name__})")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Directory Walker
# ============================================================

import os
from pathlib import Path

def walk_directory(path: str) -> Generator[Path, None, None]:
    """
    Recursively walk directory and yield all file paths.
    
    TODO: Implement recursive directory walker with yield from
    """
    path_obj = Path(path)
    
    for item in path_obj.iterdir():
        if item.is_file():
            yield item
        elif item.is_dir():
            # Recursively walk subdirectories
            yield from walk_directory(item)

def test_directory_walker():
    """Test directory walker"""
    print("--- Exercise 7: Directory Walker ---")
    
    # Create test directory structure
    test_dir = Path("test_dir")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "file1.txt").write_text("content1")
    (test_dir / "file2.txt").write_text("content2")
    
    subdir = test_dir / "subdir"
    subdir.mkdir(exist_ok=True)
    (subdir / "file3.txt").write_text("content3")
    
    # Walk directory
    print(f"Files in {test_dir}:")
    for file_path in walk_directory(test_dir):
        print(f"  {file_path}")
    
    # Cleanup
    import shutil
    shutil.rmtree(test_dir)
    
    print()

# ============================================================
# EXERCISE 8: Generator Pipeline with yield from
# ============================================================

def read_logs(filename: str) -> Generator[str, None, None]:
    """Read log lines"""
    with open(filename, 'r') as f:
        yield from f

def parse_log_line(line: str) -> dict:
    """Parse a log line"""
    parts = line.strip().split('|')
    if len(parts) == 3:
        return {
            'level': parts[0],
            'timestamp': parts[1],
            'message': parts[2]
        }
    return None

def parse_logs(filename: str) -> Generator[dict, None, None]:
    """
    Parse log file into structured data.
    
    TODO: Use yield from to read and parse
    """
    for line in read_logs(filename):
        parsed = parse_log_line(line)
        if parsed:
            yield parsed

def filter_errors(logs: Generator[dict, None, None]) -> Generator[dict, None, None]:
    """Filter error logs"""
    for log in logs:
        if log['level'] == 'ERROR':
            yield log

def test_log_pipeline():
    """Test log processing pipeline"""
    print("--- Exercise 8: Log Processing Pipeline ---")
    
    # Create test log file
    test_file = "test_logs.txt"
    with open(test_file, 'w') as f:
        f.write("INFO|2024-01-01 10:00:00|Application started\n")
        f.write("ERROR|2024-01-01 10:00:01|Database connection failed\n")
        f.write("INFO|2024-01-01 10:00:02|Retrying connection\n")
        f.write("ERROR|2024-01-01 10:00:03|Connection timeout\n")
    
    # Process logs
    print("Error logs:")
    for log in filter_errors(parse_logs(test_file)):
        print(f"  [{log['timestamp']}] {log['message']}")
    
    # Cleanup
    os.remove(test_file)
    
    print()

# ============================================================
# BONUS CHALLENGE: Recursive Data Structure
# ============================================================

def traverse_json(data: Any, path: str = "") -> Generator[tuple, None, None]:
    """
    Recursively traverse JSON-like structure.
    
    TODO: Yield (path, value) pairs for all leaf nodes
    """
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = f"{path}.{key}" if path else key
            yield from traverse_json(value, new_path)
    elif isinstance(data, list):
        for i, value in enumerate(data):
            new_path = f"{path}[{i}]"
            yield from traverse_json(value, new_path)
    else:
        # Leaf node
        yield (path, data)

def test_json_traversal():
    """Test JSON traversal"""
    print("--- Bonus Challenge: JSON Traversal ---")
    
    data = {
        "user": {
            "name": "Alice",
            "age": 30,
            "addresses": [
                {"city": "NYC", "zip": "10001"},
                {"city": "LA", "zip": "90001"}
            ]
        },
        "active": True
    }
    
    print("Leaf nodes:")
    for path, value in traverse_json(data):
        print(f"  {path}: {value}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    yield from:
    - Time: O(n) to yield n items from delegated generator
    - Space: O(1) - no additional space for delegation
    - vs manual loop: Same complexity, cleaner syntax
    
    Recursive Generators:
    - Time: O(n) where n is total items in structure
    - Space: O(d) where d is depth (call stack)
    - Flattening: O(n) time, O(d) space
    - Tree traversal: O(n) time, O(h) space (h = height)
    
    Benefits of yield from:
    - Cleaner, more readable code
    - Proper exception propagation
    - Can capture return values from sub-generators
    - Enables true generator delegation
    
    Use Cases:
    - Flattening nested structures
    - Tree/graph traversal
    - Composing multiple generators
    - Recursive data processing
    - Building parser combinators
    
    Security Considerations:
    - Recursive generators can cause stack overflow
    - Limit recursion depth for untrusted input
    - Validate nested structure depth
    - Use iterative approach for very deep structures
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 2, Day 5: yield from and Generator Delegation")
    print("=" * 60)
    print()
    
    yield_from_basics()
    test_flatten()
    test_tree_traversal()
    test_multi_file_reader()
    test_return_values()
    test_parser()
    test_directory_walker()
    test_log_pipeline()
    test_json_traversal()
    
    print("=" * 60)
    print("✅ Day 5 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. yield from delegates to another generator")
    print("2. Perfect for recursive generators and flattening")
    print("3. Can capture return values from sub-generators")
    print("4. Makes code cleaner and more composable")

