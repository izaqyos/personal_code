"""
Week 1, Day 7: Review & Mini-Challenge

Learning Objectives:
- Review all Week 1 concepts
- Apply multiple Pythonic idioms together
- Refactor imperative code to Pythonic style
- Practice real-world scenarios

Challenge: Refactor a non-Pythonic codebase to use all Week 1 idioms

Time: 15-20 minutes
"""

import time
import sys
from collections import defaultdict, Counter
from typing import List, Dict, Tuple, Optional

# ============================================================
# REVIEW: Week 1 Concepts
# ============================================================

def week1_review():
    """
    Quick review of all Week 1 concepts.
    """
    print("=" * 60)
    print("WEEK 1 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: List Comprehensions vs Generator Expressions")
    print("  • List comp: [x*2 for x in range(10)]")
    print("  • Generator: (x*2 for x in range(10))")
    print("  • Use generators for large datasets")
    
    print("\nDay 2: Dictionary Comprehensions and defaultdict")
    print("  • Dict comp: {k: v*2 for k, v in data.items()}")
    print("  • defaultdict(list) for grouping")
    print("  • Counter for frequency counting")
    
    print("\nDay 3: Unpacking and Tuple Swapping")
    print("  • a, b = b, a  # swap")
    print("  • first, *rest, last = items")
    print("  • for name, age in users: ...")
    
    print("\nDay 4: Context Managers")
    print("  • with open(file) as f: ...")
    print("  • __enter__ and __exit__ methods")
    print("  • Guaranteed resource cleanup")
    
    print("\nDay 5: EAFP vs LBYL")
    print("  • EAFP: try/except (Pythonic)")
    print("  • LBYL: if checks before action")
    print("  • EAFP is better for race conditions")
    
    print("\nDay 6: Chaining and Walrus Operator")
    print("  • if 18 <= age <= 65: ...")
    print("  • if (n := len(items)) > 10: ...")
    print("  • Use := to avoid recomputation")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: Refactor Non-Pythonic Code
# ============================================================

def challenge1_before():
    """
    NON-PYTHONIC CODE - Needs refactoring
    
    Task: Analyze a list of transactions and generate a report
    """
    print("--- Challenge 1: BEFORE (Non-Pythonic) ---")
    
    # Sample data: (user_id, amount, category, timestamp)
    transactions = [
        (1, 100.0, "food", 1234567890),
        (2, 50.0, "transport", 1234567891),
        (1, 75.0, "food", 1234567892),
        (3, 200.0, "entertainment", 1234567893),
        (2, 30.0, "food", 1234567894),
        (1, 120.0, "transport", 1234567895),
        (3, 80.0, "food", 1234567896),
    ]
    
    # Non-Pythonic approach
    user_totals = {}
    category_totals = {}
    user_categories = {}
    
    # Iterate and build dictionaries
    for i in range(len(transactions)):
        transaction = transactions[i]
        user_id = transaction[0]
        amount = transaction[1]
        category = transaction[2]
        
        # Update user totals
        if user_id in user_totals:
            user_totals[user_id] = user_totals[user_id] + amount
        else:
            user_totals[user_id] = amount
        
        # Update category totals
        if category in category_totals:
            category_totals[category] = category_totals[category] + amount
        else:
            category_totals[category] = amount
        
        # Track user categories
        if user_id not in user_categories:
            user_categories[user_id] = []
        if category not in user_categories[user_id]:
            user_categories[user_id].append(category)
    
    # Find top spender
    max_amount = 0
    top_user = None
    for user_id in user_totals:
        if user_totals[user_id] > max_amount:
            max_amount = user_totals[user_id]
            top_user = user_id
    
    print(f"User totals: {user_totals}")
    print(f"Category totals: {category_totals}")
    print(f"Top spender: User {top_user} (${max_amount})")
    print()

def challenge1_after():
    """
    PYTHONIC CODE - Refactored version
    
    TODO: Refactor using Week 1 idioms:
    - Unpacking in loops
    - defaultdict/Counter
    - Dict comprehensions
    - max() with key parameter
    """
    print("--- Challenge 1: AFTER (Pythonic) ---")
    
    transactions = [
        (1, 100.0, "food", 1234567890),
        (2, 50.0, "transport", 1234567891),
        (1, 75.0, "food", 1234567892),
        (3, 200.0, "entertainment", 1234567893),
        (2, 30.0, "food", 1234567894),
        (1, 120.0, "transport", 1234567895),
        (3, 80.0, "food", 1234567896),
    ]
    
    # TODO: Refactor using Pythonic idioms
    
    # Use defaultdict for accumulation
    user_totals = defaultdict(float)
    category_totals = defaultdict(float)
    user_categories = defaultdict(set)
    
    # Unpack in loop
    for user_id, amount, category, _ in transactions:
        user_totals[user_id] += amount
        category_totals[category] += amount
        user_categories[user_id].add(category)
    
    # Find top spender using max with key
    top_user = max(user_totals, key=user_totals.get)
    max_amount = user_totals[top_user]
    
    print(f"User totals: {dict(user_totals)}")
    print(f"Category totals: {dict(category_totals)}")
    print(f"Top spender: User {top_user} (${max_amount})")
    print()

# ============================================================
# CHALLENGE 2: Data Processing Pipeline
# ============================================================

def challenge2_data_pipeline():
    """
    Build a data processing pipeline using multiple idioms.
    
    Task: Process log entries and generate statistics
    
    TODO: Use generators, comprehensions, Counter, unpacking
    """
    print("--- Challenge 2: Data Processing Pipeline ---")
    
    # Simulated log entries
    def generate_logs(n=1000):
        """Generate sample log entries"""
        import random
        levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        services = ["api", "database", "cache", "queue"]
        
        for i in range(n):
            level = random.choice(levels)
            service = random.choice(services)
            response_time = random.randint(10, 500)
            yield f"{level}|{service}|{response_time}|message_{i}"
    
    # TODO: Process logs using Pythonic idioms
    
    # Parse logs using generator expression and unpacking
    parsed_logs = (
        (level, service, int(response_time))
        for line in generate_logs(1000)
        if (parts := line.split('|')) and len(parts) >= 3
        for level, service, response_time in [parts[:3]]
    )
    
    # Collect statistics
    error_services = defaultdict(int)
    service_times = defaultdict(list)
    level_counts = Counter()
    
    for level, service, response_time in parsed_logs:
        level_counts[level] += 1
        service_times[service].append(response_time)
        
        if level == "ERROR":
            error_services[service] += 1
    
    # Calculate averages using dict comprehension
    avg_response_times = {
        service: sum(times) / len(times)
        for service, times in service_times.items()
    }
    
    # Results
    print(f"Level counts: {dict(level_counts.most_common())}")
    print(f"Error counts by service: {dict(error_services)}")
    print(f"Average response times: {avg_response_times}")
    
    # Find slowest service
    slowest = max(avg_response_times, key=avg_response_times.get)
    print(f"Slowest service: {slowest} ({avg_response_times[slowest]:.2f}ms)")
    
    print()

# ============================================================
# CHALLENGE 3: Custom Context Manager
# ============================================================

class PerformanceMonitor:
    """
    A context manager that tracks performance metrics.
    
    TODO: Implement __enter__ and __exit__
    Track: execution time, memory usage, and exceptions
    """
    
    def __init__(self, operation_name: str):
        self.operation_name = operation_name
        self.start_time = None
        self.start_memory = None
        self.metrics = {}
    
    def __enter__(self):
        """Start monitoring"""
        # TODO: Record start metrics
        self.start_time = time.perf_counter()
        self.start_memory = sys.getsizeof([])  # Simplified
        print(f"📊 Starting: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop monitoring and report"""
        # TODO: Calculate and report metrics
        duration = time.perf_counter() - self.start_time
        
        self.metrics = {
            "duration": duration,
            "success": exc_type is None,
            "error": str(exc_val) if exc_val else None
        }
        
        print(f"📊 Finished: {self.operation_name}")
        print(f"   Duration: {duration:.4f}s")
        print(f"   Success: {self.metrics['success']}")
        
        return False

def challenge3_performance_monitoring():
    """Test the PerformanceMonitor"""
    print("--- Challenge 3: Performance Monitoring ---")
    
    # TODO: Use the PerformanceMonitor context manager
    
    with PerformanceMonitor("Data processing"):
        # Simulate work
        data = [i ** 2 for i in range(100000)]
        result = sum(data)
    
    print()

# ============================================================
# CHALLENGE 4: Combining All Idioms
# ============================================================

def challenge4_comprehensive():
    """
    Comprehensive challenge using ALL Week 1 idioms.
    
    Task: Build a user activity analyzer
    
    TODO: Use:
    - Generators for memory efficiency
    - defaultdict/Counter for aggregation
    - Unpacking in loops
    - Context managers for resources
    - EAFP for error handling
    - Walrus operator to avoid recomputation
    - Comparison chaining for validation
    """
    print("--- Challenge 4: Comprehensive Analysis ---")
    
    # Sample user activity data
    activities = [
        {"user": "alice", "action": "login", "duration": 120, "timestamp": 1000},
        {"user": "bob", "action": "view", "duration": 45, "timestamp": 1001},
        {"user": "alice", "action": "view", "duration": 60, "timestamp": 1002},
        {"user": "charlie", "action": "login", "duration": 90, "timestamp": 1003},
        {"user": "bob", "action": "purchase", "duration": 180, "timestamp": 1004},
        {"user": "alice", "action": "purchase", "duration": 200, "timestamp": 1005},
        {"user": "charlie", "action": "view", "duration": 30, "timestamp": 1006},
        {"user": "bob", "action": "view", "duration": 50, "timestamp": 1007},
    ]
    
    # TODO: Analyze activities using Pythonic idioms
    
    # Use defaultdict for grouping
    user_actions = defaultdict(list)
    user_durations = defaultdict(list)
    action_counts = Counter()
    
    # Unpack and process with EAFP
    for activity in activities:
        try:
            user = activity["user"]
            action = activity["action"]
            duration = activity["duration"]
            
            # Validate duration using chaining
            if 0 < duration <= 300:
                user_actions[user].append(action)
                user_durations[user].append(duration)
                action_counts[action] += 1
        except KeyError as e:
            print(f"  ⚠️  Skipping invalid activity: missing {e}")
    
    # Calculate statistics using comprehensions and walrus
    user_stats = {
        user: {
            "total_actions": len(actions),
            "total_duration": sum(user_durations[user]),
            "avg_duration": sum(user_durations[user]) / len(user_durations[user])
        }
        for user, actions in user_actions.items()
        if len(actions) > 0  # Guard against division by zero
    }
    
    # Find most active user
    most_active = max(user_stats, key=lambda u: user_stats[u]["total_actions"])
    
    # Report results
    print("User Statistics:")
    for user, stats in user_stats.items():
        print(f"  {user}:")
        print(f"    Actions: {stats['total_actions']}")
        print(f"    Total time: {stats['total_duration']}s")
        print(f"    Avg time: {stats['avg_duration']:.2f}s")
    
    print(f"\nMost active user: {most_active}")
    print(f"Action distribution: {dict(action_counts.most_common())}")
    
    print()

# ============================================================
# BONUS: Performance Comparison
# ============================================================

def bonus_performance_comparison():
    """
    Compare performance of Pythonic vs non-Pythonic code.
    """
    print("--- Bonus: Performance Comparison ---")
    
    data = list(range(100000))
    
    # Non-Pythonic: Manual iteration
    start = time.perf_counter()
    result1 = []
    for i in range(len(data)):
        if data[i] % 2 == 0:
            result1.append(data[i] ** 2)
    time1 = time.perf_counter() - start
    
    # Pythonic: List comprehension
    start = time.perf_counter()
    result2 = [x ** 2 for x in data if x % 2 == 0]
    time2 = time.perf_counter() - start
    
    # Pythonic: Generator (memory efficient)
    start = time.perf_counter()
    result3 = list(x ** 2 for x in data if x % 2 == 0)
    time3 = time.perf_counter() - start
    
    print(f"Non-Pythonic (manual loop): {time1:.6f}s")
    print(f"Pythonic (list comp):       {time2:.6f}s ({time1/time2:.2f}x faster)")
    print(f"Pythonic (generator):       {time3:.6f}s ({time1/time3:.2f}x faster)")
    
    print(f"\nMemory usage:")
    print(f"  List: {sys.getsizeof(result2)} bytes")
    gen = (x ** 2 for x in data if x % 2 == 0)
    print(f"  Generator: {sys.getsizeof(gen)} bytes")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """
    Self-assessment checklist for Week 1.
    """
    print("=" * 60)
    print("WEEK 1 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("List comprehensions vs generators", "Can you explain when to use each?"),
        ("Dictionary comprehensions", "Can you transform dicts in one line?"),
        ("defaultdict and Counter", "Do you know when to use each?"),
        ("Unpacking and * operator", "Can you unpack nested structures?"),
        ("Context managers", "Can you implement __enter__ and __exit__?"),
        ("EAFP vs LBYL", "Do you know which is more Pythonic?"),
        ("Comparison chaining", "Can you write: 0 <= x < 100?"),
        ("Walrus operator", "Do you know when := is useful?"),
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
    print("Week 1, Day 7: Review & Mini-Challenge")
    print("=" * 60)
    print()
    
    week1_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    challenge1_before()
    challenge1_after()
    challenge2_data_pipeline()
    challenge3_performance_monitoring()
    challenge4_comprehensive()
    bonus_performance_comparison()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 1 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered Pythonic idioms!")
    print("\n📚 Next: Week 2 - Iterator Protocol & Generators")
    print("\n💡 Keep practicing these idioms in your daily code!")

