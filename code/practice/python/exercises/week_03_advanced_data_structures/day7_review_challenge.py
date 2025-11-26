"""
Week 3, Day 7: Review & Challenge - Implement LRU Cache

Learning Objectives:
- Review all Week 3 concepts (Counter, deque, defaultdict, OrderedDict, ChainMap, namedtuple)
- Build a complete LRU cache using collections
- Apply multiple data structures together
- Practice real-world system design

Challenge: Build a production-ready LRU Cache with statistics

Time: 15-20 minutes
"""

from collections import Counter, deque, defaultdict, OrderedDict, namedtuple
from typing import Any, Optional, NamedTuple
import time

# ============================================================
# REVIEW: Week 3 Concepts
# ============================================================

def week3_review():
    """
    Quick review of all Week 3 concepts.
    """
    print("=" * 60)
    print("WEEK 3 REVIEW")
    print("=" * 60)
    
    print("\nDay 1: Counter")
    print("  • Frequency counting: Counter(iterable)")
    print("  • most_common(n) for top items")
    print("  • Arithmetic: +, -, &, |")
    
    print("\nDay 2: deque")
    print("  • O(1) append/pop from both ends")
    print("  • rotate() for round-robin")
    print("  • maxlen for bounded queues")
    
    print("\nDay 3: defaultdict")
    print("  • Auto-creates missing keys with factory")
    print("  • defaultdict(list) for grouping")
    print("  • defaultdict(int) for counting")
    
    print("\nDay 4: OrderedDict")
    print("  • Maintains insertion order (dict does too in 3.7+)")
    print("  • move_to_end() for LRU patterns")
    print("  • popitem(last=False) for FIFO")
    
    print("\nDay 5: ChainMap")
    print("  • Layered dictionary lookups")
    print("  • new_child() for nested scopes")
    print("  • Perfect for config hierarchies")
    
    print("\nDay 6: namedtuple")
    print("  • Immutable records with named fields")
    print("  • typing.NamedTuple for type hints")
    print("  • _replace() for updates")
    
    print("\n" + "=" * 60)
    print()

# ============================================================
# CHALLENGE 1: LRU Cache with Statistics
# ============================================================

class CacheStats(NamedTuple):
    """Cache statistics"""
    hits: int
    misses: int
    evictions: int
    current_size: int
    
    def hit_rate(self) -> float:
        """Calculate hit rate"""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0.0

class LRUCache:
    """
    LRU (Least Recently Used) Cache implementation.
    
    TODO: Implement using OrderedDict for O(1) operations
    """
    
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self.cache = OrderedDict()
        
        # Statistics
        self.hits = 0
        self.misses = 0
        self.evictions = 0
    
    def get(self, key: Any) -> Optional[Any]:
        """Get value from cache"""
        if key in self.cache:
            # Hit: move to end (most recent)
            self.cache.move_to_end(key)
            self.hits += 1
            return self.cache[key]
        else:
            # Miss
            self.misses += 1
            return None
    
    def put(self, key: Any, value: Any):
        """Put value in cache"""
        if key in self.cache:
            # Update existing
            self.cache.move_to_end(key)
        else:
            # Add new
            if len(self.cache) >= self.maxsize:
                # Evict LRU (first item)
                self.cache.popitem(last=False)
                self.evictions += 1
        
        self.cache[key] = value
    
    def stats(self) -> CacheStats:
        """Get cache statistics"""
        return CacheStats(
            hits=self.hits,
            misses=self.misses,
            evictions=self.evictions,
            current_size=len(self.cache)
        )
    
    def clear(self):
        """Clear cache"""
        self.cache.clear()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

def test_lru_cache():
    """Test LRU cache"""
    print("--- Challenge 1: LRU Cache with Statistics ---")
    
    cache = LRUCache(maxsize=3)
    
    # Add items
    print("Adding items:")
    cache.put('a', 1)
    cache.put('b', 2)
    cache.put('c', 3)
    print(f"  Cache: {list(cache.cache.keys())}")
    
    # Access 'a' (makes it recent)
    val = cache.get('a')
    print(f"\nAccess 'a': {val}")
    print(f"  Cache: {list(cache.cache.keys())}")
    
    # Add 'd' (evicts 'b')
    cache.put('d', 4)
    print(f"\nAdd 'd' (evicts LRU):")
    print(f"  Cache: {list(cache.cache.keys())}")
    
    # Try to get 'b' (miss)
    val = cache.get('b')
    print(f"\nAccess 'b': {val} (evicted)")
    
    # Statistics
    stats = cache.stats()
    print(f"\nCache statistics:")
    print(f"  Hits: {stats.hits}")
    print(f"  Misses: {stats.misses}")
    print(f"  Evictions: {stats.evictions}")
    print(f"  Hit rate: {stats.hit_rate():.2%}")
    print(f"  Current size: {stats.current_size}/{cache.maxsize}")
    
    print()

# ============================================================
# CHALLENGE 2: Word Frequency Analyzer
# ============================================================

class WordFrequencyAnalyzer:
    """
    Analyze word frequencies with various statistics.
    
    TODO: Use Counter, defaultdict, and namedtuple
    """
    
    def __init__(self):
        self.word_count = Counter()
        self.word_positions = defaultdict(list)
        self.total_words = 0
    
    def add_text(self, text: str):
        """Add text to analyzer"""
        words = text.lower().split()
        
        for position, word in enumerate(words, start=self.total_words):
            self.word_count[word] += 1
            self.word_positions[word].append(position)
        
        self.total_words += len(words)
    
    def most_common(self, n: int = 10):
        """Get most common words"""
        return self.word_count.most_common(n)
    
    def word_stats(self, word: str):
        """Get statistics for a word"""
        WordStats = namedtuple('WordStats', ['word', 'count', 'frequency', 'positions'])
        
        count = self.word_count[word]
        frequency = count / self.total_words if self.total_words > 0 else 0
        positions = self.word_positions[word]
        
        return WordStats(word, count, frequency, positions)
    
    def words_by_length(self):
        """Group words by length"""
        by_length = defaultdict(list)
        for word in self.word_count:
            by_length[len(word)].append(word)
        return dict(by_length)

def test_word_analyzer():
    """Test word frequency analyzer"""
    print("--- Challenge 2: Word Frequency Analyzer ---")
    
    analyzer = WordFrequencyAnalyzer()
    
    text = """
    Python is an amazing programming language. Python is easy to learn
    and Python is powerful. Many developers love Python because Python
    has a simple syntax. Python rocks!
    """
    
    analyzer.add_text(text)
    
    print("Top 5 words:")
    for word, count in analyzer.most_common(5):
        print(f"  {word}: {count}")
    
    # Detailed stats for 'python'
    stats = analyzer.word_stats('python')
    print(f"\nStats for '{stats.word}':")
    print(f"  Count: {stats.count}")
    print(f"  Frequency: {stats.frequency:.2%}")
    print(f"  Positions: {stats.positions[:5]}...")  # First 5
    
    # Words by length
    by_length = analyzer.words_by_length()
    print(f"\nWords by length:")
    for length in sorted(by_length.keys())[:5]:
        words = by_length[length][:3]  # First 3
        print(f"  {length} letters: {words}")
    
    print()

# ============================================================
# CHALLENGE 3: Request Rate Limiter
# ============================================================

class RateLimiter:
    """
    Rate limiter using deque for sliding window.
    
    TODO: Implement sliding window rate limiter
    """
    
    def __init__(self, max_requests: int, window_seconds: float):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(deque)  # user_id -> timestamps
    
    def allow_request(self, user_id: str) -> bool:
        """Check if request is allowed"""
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Remove old requests outside window
        while user_requests and user_requests[0] < now - self.window_seconds:
            user_requests.popleft()
        
        # Check if under limit
        if len(user_requests) < self.max_requests:
            user_requests.append(now)
            return True
        
        return False
    
    def get_stats(self, user_id: str):
        """Get user statistics"""
        now = time.time()
        user_requests = self.requests[user_id]
        
        # Clean old requests
        while user_requests and user_requests[0] < now - self.window_seconds:
            user_requests.popleft()
        
        return {
            'requests_in_window': len(user_requests),
            'max_requests': self.max_requests,
            'window_seconds': self.window_seconds,
            'can_request': len(user_requests) < self.max_requests
        }

def test_rate_limiter():
    """Test rate limiter"""
    print("--- Challenge 3: Rate Limiter ---")
    
    # Allow 3 requests per 2 seconds
    limiter = RateLimiter(max_requests=3, window_seconds=2.0)
    
    user = "user123"
    
    print(f"Rate limit: 3 requests per 2 seconds")
    print("\nMaking requests:")
    
    for i in range(5):
        allowed = limiter.allow_request(user)
        stats = limiter.get_stats(user)
        status = "✓ Allowed" if allowed else "✗ Blocked"
        print(f"  Request {i+1}: {status} ({stats['requests_in_window']}/{stats['max_requests']})")
        time.sleep(0.3)
    
    print("\nWaiting 2 seconds...")
    time.sleep(2.0)
    
    print("\nAfter window reset:")
    allowed = limiter.allow_request(user)
    stats = limiter.get_stats(user)
    print(f"  Request: {'✓ Allowed' if allowed else '✗ Blocked'} ({stats['requests_in_window']}/{stats['max_requests']})")
    
    print()

# ============================================================
# CHALLENGE 4: Configuration Manager
# ============================================================

class ConfigurationManager:
    """
    Multi-level configuration with ChainMap and defaults.
    
    TODO: Implement config manager with multiple sources
    """
    
    def __init__(self):
        # Defaults (lowest priority)
        self.defaults = {
            'debug': False,
            'log_level': 'INFO',
            'timeout': 30,
            'max_retries': 3
        }
        
        # User config
        self.user_config = {}
        
        # Environment overrides
        self.env_config = {}
        
        # Build chain
        self._rebuild_chain()
        
        # Track access for statistics
        self.access_count = Counter()
    
    def _rebuild_chain(self):
        """Rebuild configuration chain"""
        from collections import ChainMap
        self.config = ChainMap(
            self.env_config,
            self.user_config,
            self.defaults
        )
    
    def get(self, key: str, default=None):
        """Get configuration value"""
        self.access_count[key] += 1
        return self.config.get(key, default)
    
    def set_user(self, key: str, value: Any):
        """Set user configuration"""
        self.user_config[key] = value
        self._rebuild_chain()
    
    def set_env(self, key: str, value: Any):
        """Set environment configuration"""
        self.env_config[key] = value
        self._rebuild_chain()
    
    def get_source(self, key: str) -> str:
        """Get which level provides the value"""
        if key in self.env_config:
            return "environment"
        elif key in self.user_config:
            return "user"
        elif key in self.defaults:
            return "default"
        return "not found"
    
    def most_accessed(self, n: int = 5):
        """Get most accessed config keys"""
        return self.access_count.most_common(n)

def test_config_manager():
    """Test configuration manager"""
    print("--- Challenge 4: Configuration Manager ---")
    
    config = ConfigurationManager()
    
    # Set user preferences
    config.set_user('debug', True)
    config.set_user('timeout', 60)
    
    # Set environment overrides
    config.set_env('log_level', 'DEBUG')
    
    # Access configurations
    print("Configuration values:")
    for key in ['debug', 'log_level', 'timeout', 'max_retries']:
        value = config.get(key)
        source = config.get_source(key)
        print(f"  {key}: {value} (from {source})")
    
    # Access some keys multiple times
    config.get('debug')
    config.get('debug')
    config.get('timeout')
    
    print("\nMost accessed configs:")
    for key, count in config.most_accessed(3):
        print(f"  {key}: {count} times")
    
    print()

# ============================================================
# CHALLENGE 5: Comprehensive Data Pipeline
# ============================================================

def comprehensive_pipeline():
    """
    Build a data pipeline using multiple collections.
    
    TODO: Process log data with all Week 3 tools
    """
    print("--- Challenge 5: Comprehensive Data Pipeline ---")
    
    # Simulated log entries
    LogEntry = namedtuple('LogEntry', ['timestamp', 'level', 'service', 'message', 'response_time'])
    
    logs = [
        LogEntry(1000, 'ERROR', 'api', 'Connection failed', 500),
        LogEntry(1001, 'INFO', 'api', 'Request processed', 45),
        LogEntry(1002, 'ERROR', 'database', 'Query timeout', 300),
        LogEntry(1003, 'WARNING', 'cache', 'Cache miss', 10),
        LogEntry(1004, 'ERROR', 'api', 'Invalid request', 5),
        LogEntry(1005, 'INFO', 'database', 'Query executed', 120),
        LogEntry(1006, 'ERROR', 'api', 'Connection failed', 500),
    ]
    
    # Count errors by service using Counter
    error_counts = Counter(
        log.service for log in logs if log.level == 'ERROR'
    )
    
    print("Errors by service:")
    for service, count in error_counts.most_common():
        print(f"  {service}: {count}")
    
    # Group logs by level using defaultdict
    by_level = defaultdict(list)
    for log in logs:
        by_level[log.level].append(log)
    
    print("\nLogs by level:")
    for level, entries in by_level.items():
        avg_time = sum(e.response_time for e in entries) / len(entries)
        print(f"  {level}: {len(entries)} entries, avg time: {avg_time:.1f}ms")
    
    # Track recent errors using deque
    recent_errors = deque(maxlen=3)
    for log in logs:
        if log.level == 'ERROR':
            recent_errors.append(log)
    
    print("\nRecent errors (last 3):")
    for log in recent_errors:
        print(f"  [{log.timestamp}] {log.service}: {log.message}")
    
    print()

# ============================================================
# PERFORMANCE COMPARISON
# ============================================================

def performance_summary():
    """
    Summary of performance characteristics.
    """
    print("--- Performance Summary ---")
    
    print("Operation Complexity:")
    print("  Counter.most_common(k): O(n log k)")
    print("  deque.append/popleft: O(1)")
    print("  defaultdict[key]: O(1)")
    print("  OrderedDict.move_to_end: O(1)")
    print("  ChainMap lookup: O(m) where m = # of maps")
    print("  namedtuple access: O(1)")
    
    print("\nMemory Efficiency:")
    print("  Counter: O(unique items)")
    print("  deque: O(n)")
    print("  defaultdict: O(unique keys)")
    print("  OrderedDict: O(n) + linked list overhead")
    print("  ChainMap: O(1) - just references")
    print("  namedtuple: O(fields) - like tuple")
    
    print()

# ============================================================
# SELF-ASSESSMENT
# ============================================================

def self_assessment():
    """
    Self-assessment checklist for Week 3.
    """
    print("=" * 60)
    print("WEEK 3 SELF-ASSESSMENT")
    print("=" * 60)
    
    checklist = [
        ("Counter", "Can you count frequencies and find top items?"),
        ("deque", "Do you know when to use deque vs list?"),
        ("defaultdict", "Can you eliminate KeyError checks?"),
        ("OrderedDict", "Do you know when it's still useful?"),
        ("ChainMap", "Can you implement layered lookups?"),
        ("namedtuple", "Can you create immutable records?"),
        ("Combining tools", "Can you use multiple collections together?"),
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
    print("Week 3, Day 7: Review & Challenge")
    print("=" * 60)
    print()
    
    week3_review()
    
    print("\n" + "=" * 60)
    print("CHALLENGES")
    print("=" * 60 + "\n")
    
    test_lru_cache()
    test_word_analyzer()
    test_rate_limiter()
    test_config_manager()
    comprehensive_pipeline()
    performance_summary()
    
    self_assessment()
    
    print("=" * 60)
    print("✅ Week 3 Complete!")
    print("=" * 60)
    print("\n🎉 Congratulations! You've mastered collections!")
    print("\n📚 Next: Week 4 - Functional Programming")
    print("\n💡 Keep using these tools for cleaner, more efficient code!")

