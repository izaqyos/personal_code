"""
Week 2, Day 7: Review & Challenge - Build a Custom Data Pipeline

Learning Objectives:
- Review all Week 2 concepts
- Build a complete data processing pipeline
- Combine iterators, generators, and itertools
- Apply best practices for memory efficiency

Challenge: Build a log analysis system using all Week 2 concepts

Time: 15-20 minutes
"""

import itertools
from collections import defaultdict, Counter
from typing import Generator, Iterable, Any
import time

# ============================================================
# REVIEW: Week 2 Concepts
# ============================================================

def week2_review():
    """
    Quick review of all Week 2 concepts.
    """
    print("=" * 60)
    print("WEEK 2 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Custom Iterators")
    print("  • __iter__() and __next__() protocol")
    print("  • Raise StopIteration when done")
    print("  • Separate iterable from iterator for reusability")
    
    print("\nDay 2: Generator Functions")
    print("  • Use 'yield' to create generators")
    print("  • Generators are memory efficient (O(1) space)")
    print("  • Can send() values to generators")
    
    print("\nDay 3: itertools Module")
    print("  • islice, chain, groupby for efficient processing")
    print("  • Combinatorics: product, permutations, combinations")
    print("  • Infinite: count, cycle, repeat")
    
    print("\nDay 4: Generator Pipelines")
    print("  • Chain generator expressions")
    print("  • Each stage: O(1) space")
    print("  • Lazy evaluation throughout")
    
    print("\nDay 5: yield from")
    print("  • Delegate to another generator")
    print("  • Perfect for recursive generators")
    print("  • Can capture return values")
    
    print("\nDay 6: Infinite Generators")
    print("  • Represent infinite sequences")
    print("  • ALWAYS limit with islice/takewhile")
    print("  • Use for streams and continuous data")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Custom Iterator with State
# ============================================================

class MovingAverage:
    """
    Iterator that computes moving average over a window.
    
    TODO: Implement custom iterator with sliding window
    """
    
    def __init__(self, data: Iterable, window_size: int):
        self.data = iter(data)
        self.window_size = window_size
        self.window = []
    
    def __iter__(self):
        return self
    
    def __next__(self):
        """Return next moving average"""
        # TODO: Implement moving average logic
        try:
            value = next(self.data)
            self.window.append(value)
            
            if len(self.window) > self.window_size:
                self.window.pop(0)
            
            return sum(self.window) / len(self.window)
        except StopIteration:
            raise StopIteration

def test_moving_average():
    """Test the MovingAverage iterator"""
    print("--- Challenge 1: Moving Average Iterator ---")
    
    data = [10, 20, 30, 40, 50, 60, 70, 80]
    window = 3
    
    print(f"Data: {data}")
    print(f"Moving average (window={window}):")
    for avg in MovingAverage(data, window):
        print(f"  {avg:.2f}")
    
    print()

# ============================================================
# CHALLENGE 2: Log Processing Pipeline
# ============================================================

def generate_logs(n: int) -> Generator[str, None, None]:
    """
    Generate sample log entries.
    
    TODO: Generate realistic log data
    """
    import random
    levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
    services = ["api", "database", "cache", "queue"]
    messages = [
        "Request processed",
        "Connection established",
        "Operation failed",
        "Timeout occurred",
        "Data cached",
        "Query executed"
    ]
    
    for i in range(n):
        level = random.choice(levels)
        service = random.choice(services)
        message = random.choice(messages)
        response_time = random.randint(10, 500)
        
        yield f"{i}|{level}|{service}|{message}|{response_time}"

def parse_log_entry(line: str) -> dict:
    """Parse a log entry"""
    parts = line.strip().split('|')
    if len(parts) == 5:
        return {
            'id': int(parts[0]),
            'level': parts[1],
            'service': parts[2],
            'message': parts[3],
            'response_time': int(parts[4])
        }
    return None

def build_log_pipeline(logs: Iterable[str]) -> Generator[dict, None, None]:
    """
    Build complete log processing pipeline.
    
    TODO: Parse, filter, and transform logs
    """
    # Parse logs
    parsed = (parse_log_entry(line) for line in logs)
    
    # Filter out None values
    valid = (log for log in parsed if log is not None)
    
    # Filter important logs (ERROR or WARNING)
    important = (log for log in valid if log['level'] in ['ERROR', 'WARNING'])
    
    # Filter slow responses (> 200ms)
    slow = (log for log in important if log['response_time'] > 200)
    
    yield from slow

def test_log_pipeline():
    """Test the log processing pipeline"""
    print("--- Challenge 2: Log Processing Pipeline ---")
    
    # Generate logs
    logs = generate_logs(1000)
    
    # Process through pipeline
    results = list(build_log_pipeline(logs))
    
    print(f"Processed 1000 logs")
    print(f"Found {len(results)} slow errors/warnings (>200ms)")
    
    # Show first 5
    print("\nFirst 5 results:")
    for log in itertools.islice(results, 5):
        print(f"  [{log['level']}] {log['service']}: "
              f"{log['message']} ({log['response_time']}ms)")
    
    print()

# ============================================================
# CHALLENGE 3: Data Aggregation with groupby
# ============================================================

def analyze_logs_by_service(logs: Iterable[str]):
    """
    Analyze logs grouped by service.
    
    TODO: Use itertools.groupby to aggregate statistics
    """
    print("--- Challenge 3: Log Analysis by Service ---")
    
    # Parse all logs
    parsed = (parse_log_entry(line) for line in logs)
    valid = [log for log in parsed if log is not None]
    
    # Sort by service (required for groupby)
    sorted_logs = sorted(valid, key=lambda x: x['service'])
    
    # Group by service
    print("Statistics by service:")
    for service, group in itertools.groupby(sorted_logs, key=lambda x: x['service']):
        logs_list = list(group)
        
        # Calculate statistics
        total = len(logs_list)
        errors = sum(1 for log in logs_list if log['level'] == 'ERROR')
        avg_time = sum(log['response_time'] for log in logs_list) / total
        
        print(f"  {service}:")
        print(f"    Total: {total}")
        print(f"    Errors: {errors}")
        print(f"    Avg response: {avg_time:.2f}ms")
    
    print()

def test_log_analysis():
    """Test log analysis"""
    logs = generate_logs(500)
    analyze_logs_by_service(logs)

# ============================================================
# CHALLENGE 4: Recursive Generator for Directory Tree
# ============================================================

class FileNode:
    """Represents a file or directory"""
    def __init__(self, name: str, is_dir: bool = False, children=None):
        self.name = name
        self.is_dir = is_dir
        self.children = children or []

def traverse_file_tree(node: FileNode, depth: int = 0) -> Generator[tuple, None, None]:
    """
    Traverse file tree and yield (depth, name, is_dir).
    
    TODO: Implement recursive traversal with yield from
    """
    # Yield current node
    yield (depth, node.name, node.is_dir)
    
    # Recursively yield children
    if node.is_dir:
        for child in node.children:
            yield from traverse_file_tree(child, depth + 1)

def test_file_tree():
    """Test file tree traversal"""
    print("--- Challenge 4: File Tree Traversal ---")
    
    # Build sample file tree
    tree = FileNode("root", is_dir=True, children=[
        FileNode("src", is_dir=True, children=[
            FileNode("main.py"),
            FileNode("utils.py"),
            FileNode("tests", is_dir=True, children=[
                FileNode("test_main.py"),
                FileNode("test_utils.py")
            ])
        ]),
        FileNode("README.md"),
        FileNode("requirements.txt")
    ])
    
    # Traverse and display
    print("File tree:")
    for depth, name, is_dir in traverse_file_tree(tree):
        indent = "  " * depth
        icon = "📁" if is_dir else "📄"
        print(f"{indent}{icon} {name}")
    
    print()

# ============================================================
# CHALLENGE 5: Infinite Data Stream with Processing
# ============================================================

def event_stream() -> Generator[dict, None, None]:
    """
    Generate infinite event stream.
    
    TODO: Create infinite event generator
    """
    import random
    
    event_types = ["click", "view", "purchase", "logout"]
    users = [f"user{i}" for i in range(1, 6)]
    
    for event_id in itertools.count(1):
        yield {
            'id': event_id,
            'type': random.choice(event_types),
            'user': random.choice(users),
            'timestamp': event_id
        }

def process_event_stream(stream: Generator, duration: int = 10):
    """
    Process event stream for limited duration.
    
    TODO: Process and aggregate events
    """
    print("--- Challenge 5: Event Stream Processing ---")
    
    # Collect events
    events = list(itertools.islice(stream, duration))
    
    # Count by type
    type_counts = Counter(event['type'] for event in events)
    
    # Count by user
    user_counts = Counter(event['user'] for event in events)
    
    print(f"Processed {len(events)} events:")
    print(f"\nBy type: {dict(type_counts)}")
    print(f"By user: {dict(user_counts)}")
    
    print()

def test_event_stream():
    """Test event stream processing"""
    stream = event_stream()
    process_event_stream(stream, duration=50)

# ============================================================
# CHALLENGE 6: Complete Data Pipeline
# ============================================================

def complete_pipeline_challenge():
    """
    Build a complete data processing pipeline combining all concepts.
    
    TODO: Process sales data through multiple stages
    """
    print("--- Challenge 6: Complete Data Pipeline ---")
    
    # Generate sales data
    def generate_sales(n):
        """Generate sample sales data"""
        import random
        products = ["laptop", "mouse", "keyboard", "monitor"]
        regions = ["north", "south", "east", "west"]
        
        for sale_id in range(1, n + 1):
            yield {
                'id': sale_id,
                'product': random.choice(products),
                'amount': random.randint(50, 2000),
                'region': random.choice(regions),
                'quantity': random.randint(1, 5)
            }
    
    # Pipeline stages
    sales = generate_sales(1000)
    
    # Stage 1: Filter high-value sales (>= 500)
    high_value = (sale for sale in sales if sale['amount'] >= 500)
    
    # Stage 2: Add total field
    with_total = (
        {**sale, 'total': sale['amount'] * sale['quantity']}
        for sale in high_value
    )
    
    # Stage 3: Collect and group by region
    sales_list = list(with_total)
    sales_by_region = sorted(sales_list, key=lambda x: x['region'])
    
    # Aggregate by region
    print("High-value sales by region:")
    for region, group in itertools.groupby(sales_by_region, key=lambda x: x['region']):
        group_list = list(group)
        total_revenue = sum(sale['total'] for sale in group_list)
        count = len(group_list)
        avg = total_revenue / count
        
        print(f"  {region.upper()}:")
        print(f"    Sales: {count}")
        print(f"    Revenue: ${total_revenue:,}")
        print(f"    Average: ${avg:,.2f}")
    
    print()

# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

def performance_comparison():
    """
    Compare different approaches for data processing.
    """
    print("--- Performance Comparison ---")
    
    n = 1_000_000
    
    # Approach 1: List-based (memory intensive)
    start = time.perf_counter()
    data = list(range(n))
    filtered = [x for x in data if x % 2 == 0]
    squared = [x**2 for x in filtered]
    result1 = squared[:100]
    time1 = time.perf_counter() - start
    
    # Approach 2: Generator-based (memory efficient)
    start = time.perf_counter()
    pipeline = (x**2 for x in range(n) if x % 2 == 0)
    result2 = list(itertools.islice(pipeline, 100))
    time2 = time.perf_counter() - start
    
    print(f"Processing {n:,} numbers, getting first 100 even squares:")
    print(f"  List-based: {time1:.4f}s")
    print(f"  Generator-based: {time2:.4f}s ({time1/time2:.2f}x faster)")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """
    Self-assessment checklist for Week 2.
    """
    print("=" * 60)
    print("WEEK 2 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Custom iterators", "Can you implement __iter__ and __next__?"),
        ("Generator functions", "Do you understand yield and its benefits?"),
        ("itertools module", "Can you use islice, chain, groupby effectively?"),
        ("Generator pipelines", "Can you chain multiple generator expressions?"),
        ("yield from", "Do you know when to use generator delegation?"),
        ("Infinite generators", "Can you create and safely limit them?"),
        ("Memory efficiency", "Do you understand O(1) vs O(n) space?"),
        ("Real-world application", "Can you build a complete data pipeline?"),
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
    print("Week 2, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week2_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    test_moving_average()
    test_log_pipeline()
    test_log_analysis()
    test_file_tree()
    test_event_stream()
    complete_pipeline_challenge()
    performance_comparison()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 2 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered iterators and generators!")
    print("\n📚 Next: Week 3 - Advanced Data Structures (collections module)")
    print("\n💡 Keep using generators for memory-efficient code!")

