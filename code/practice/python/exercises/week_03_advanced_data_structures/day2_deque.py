"""
Week 3, Day 2: deque - Efficient Queues and Rotation Operations

Learning Objectives:
- Master the deque (double-ended queue) class
- Learn efficient append/pop from both ends
- Understand rotation operations
- Practice queue and stack implementations

Time: 10-15 minutes
"""

from collections import deque
from typing import Any
import time

# ============================================================
# EXERCISE 1: deque Basics
# ============================================================

def deque_basics():
    """
    Learn basic deque operations.
    
    deque: Double-ended queue with O(1) append/pop from both ends
    """
    print("--- Exercise 1: deque Basics ---")
    
    # Create deque
    d = deque([1, 2, 3, 4, 5])
    print(f"Initial deque: {d}")
    
    # Append to right (end)
    d.append(6)
    print(f"After append(6): {d}")
    
    # Append to left (beginning)
    d.appendleft(0)
    print(f"After appendleft(0): {d}")
    
    # Pop from right
    right = d.pop()
    print(f"Popped from right: {right}, deque: {d}")
    
    # Pop from left
    left = d.popleft()
    print(f"Popped from left: {left}, deque: {d}")
    
    print()

# ============================================================
# EXERCISE 2: deque vs list Performance
# ============================================================

def performance_comparison():
    """
    Compare deque vs list for operations at both ends.
    
    TODO: Measure performance differences
    """
    print("--- Exercise 2: deque vs list Performance ---")
    
    n = 100000
    
    # List: append left (slow!)
    start = time.perf_counter()
    lst = []
    for i in range(n):
        lst.insert(0, i)  # O(n) operation!
    time_list = time.perf_counter() - start
    
    # deque: append left (fast!)
    start = time.perf_counter()
    dq = deque()
    for i in range(n):
        dq.appendleft(i)  # O(1) operation!
    time_deque = time.perf_counter() - start
    
    print(f"Inserting {n:,} items at beginning:")
    print(f"  List:  {time_list:.4f}s")
    print(f"  deque: {time_deque:.4f}s")
    print(f"  deque is {time_list/time_deque:.0f}x faster!")
    
    print()

# ============================================================
# EXERCISE 3: Rotation Operations
# ============================================================

def rotation_operations():
    """
    Use rotate() to shift elements.
    
    TODO: Practice rotation operations
    """
    print("--- Exercise 3: Rotation Operations ---")
    
    d = deque([1, 2, 3, 4, 5])
    print(f"Original: {d}")
    
    # Rotate right (positive)
    d.rotate(2)
    print(f"After rotate(2): {d}")
    
    # Rotate left (negative)
    d.rotate(-3)
    print(f"After rotate(-3): {d}")
    
    # Rotate back to original
    d.rotate(1)
    print(f"Back to original: {d}")
    
    # Use case: Round-robin scheduling
    print("\nRound-robin task assignment:")
    tasks = deque(['Task1', 'Task2', 'Task3'])
    workers = deque(['Alice', 'Bob', 'Charlie'])
    
    for _ in range(6):
        task = tasks[0]
        worker = workers[0]
        print(f"  {task} → {worker}")
        tasks.rotate(-1)
        workers.rotate(-1)
    
    print()

# ============================================================
# EXERCISE 4: maxlen - Bounded Deque
# ============================================================

def bounded_deque():
    """
    Use maxlen to create fixed-size deque.
    
    TODO: Practice bounded deque for sliding windows
    """
    print("--- Exercise 4: Bounded deque (maxlen) ---")
    
    # Create deque with max length
    recent_items = deque(maxlen=5)
    
    print("Adding items to deque with maxlen=5:")
    for i in range(8):
        recent_items.append(i)
        print(f"  Added {i}: {list(recent_items)}")
    
    # Use case: Recent history tracking
    print("\nRecent search history (max 3):")
    search_history = deque(maxlen=3)
    
    searches = ["python", "java", "rust", "go", "javascript"]
    for search in searches:
        search_history.append(search)
        print(f"  Searched '{search}': {list(search_history)}")
    
    print()

# ============================================================
# EXERCISE 5: Implementing a Queue
# ============================================================

class Queue:
    """
    Queue implementation using deque.
    
    TODO: Implement FIFO queue
    """
    
    def __init__(self):
        self._items = deque()
    
    def enqueue(self, item: Any):
        """Add item to rear of queue"""
        self._items.append(item)
    
    def dequeue(self) -> Any:
        """Remove and return item from front of queue"""
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()
    
    def peek(self) -> Any:
        """Return front item without removing"""
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return queue size"""
        return len(self._items)
    
    def __repr__(self):
        return f"Queue({list(self._items)})"

def test_queue():
    """Test the Queue implementation"""
    print("--- Exercise 5: Queue Implementation ---")
    
    q = Queue()
    
    print("Enqueuing items:")
    for i in range(1, 6):
        q.enqueue(i)
        print(f"  Enqueued {i}: {q}")
    
    print("\nDequeuing items:")
    while not q.is_empty():
        item = q.dequeue()
        print(f"  Dequeued {item}: {q}")
    
    print()

# ============================================================
# EXERCISE 6: Implementing a Stack
# ============================================================

class Stack:
    """
    Stack implementation using deque.
    
    TODO: Implement LIFO stack
    """
    
    def __init__(self):
        self._items = deque()
    
    def push(self, item: Any):
        """Push item onto stack"""
        self._items.append(item)
    
    def pop(self) -> Any:
        """Pop item from stack"""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()
    
    def peek(self) -> Any:
        """Return top item without removing"""
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty"""
        return len(self._items) == 0
    
    def size(self) -> int:
        """Return stack size"""
        return len(self._items)
    
    def __repr__(self):
        return f"Stack({list(self._items)})"

def test_stack():
    """Test the Stack implementation"""
    print("--- Exercise 6: Stack Implementation ---")
    
    s = Stack()
    
    print("Pushing items:")
    for i in range(1, 6):
        s.push(i)
        print(f"  Pushed {i}: {s}")
    
    print("\nPopping items:")
    while not s.is_empty():
        item = s.pop()
        print(f"  Popped {item}: {s}")
    
    print()

# ============================================================
# EXERCISE 7: Real-World Scenario - Browser History
# ============================================================

class BrowserHistory:
    """
    Browser history with back/forward navigation.
    
    TODO: Implement browser history using two deques
    """
    
    def __init__(self):
        self.back_stack = deque()
        self.forward_stack = deque()
        self.current = None
    
    def visit(self, url: str):
        """Visit a new URL"""
        if self.current:
            self.back_stack.append(self.current)
        self.current = url
        self.forward_stack.clear()  # Clear forward history
    
    def back(self) -> str:
        """Go back to previous page"""
        if not self.back_stack:
            return self.current
        
        self.forward_stack.append(self.current)
        self.current = self.back_stack.pop()
        return self.current
    
    def forward(self) -> str:
        """Go forward to next page"""
        if not self.forward_stack:
            return self.current
        
        self.back_stack.append(self.current)
        self.current = self.forward_stack.pop()
        return self.current
    
    def current_page(self) -> str:
        """Get current page"""
        return self.current

def test_browser_history():
    """Test browser history"""
    print("--- Exercise 7: Browser History ---")
    
    browser = BrowserHistory()
    
    # Visit pages
    pages = ["google.com", "github.com", "stackoverflow.com", "python.org"]
    print("Visiting pages:")
    for page in pages:
        browser.visit(page)
        print(f"  Visited: {page}")
    
    # Navigate back
    print("\nNavigating back:")
    for _ in range(2):
        page = browser.back()
        print(f"  Back to: {page}")
    
    # Navigate forward
    print("\nNavigating forward:")
    page = browser.forward()
    print(f"  Forward to: {page}")
    
    # Visit new page (clears forward history)
    print("\nVisiting new page:")
    browser.visit("reddit.com")
    print(f"  Current: {browser.current_page()}")
    print(f"  Can go forward? {len(browser.forward_stack) > 0}")
    
    print()

# ============================================================
# EXERCISE 8: Sliding Window with deque
# ============================================================

def sliding_window_maximum(nums: list, k: int) -> list:
    """
    Find maximum in each sliding window of size k.
    
    TODO: Implement using deque for O(n) solution
    
    Args:
        nums: List of numbers
        k: Window size
    
    Returns:
        List of maximums for each window
    """
    if not nums or k == 0:
        return []
    
    result = []
    window = deque()  # Store indices
    
    for i, num in enumerate(nums):
        # Remove indices outside window
        while window and window[0] <= i - k:
            window.popleft()
        
        # Remove smaller elements (they won't be max)
        while window and nums[window[-1]] < num:
            window.pop()
        
        window.append(i)
        
        # Add to result when window is full
        if i >= k - 1:
            result.append(nums[window[0]])
    
    return result

def test_sliding_window():
    """Test sliding window maximum"""
    print("--- Exercise 8: Sliding Window Maximum ---")
    
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    k = 3
    
    result = sliding_window_maximum(nums, k)
    
    print(f"Array: {nums}")
    print(f"Window size: {k}")
    print(f"Maximums: {result}")
    
    # Show windows
    print("\nWindow details:")
    for i in range(len(nums) - k + 1):
        window = nums[i:i+k]
        print(f"  {window} → max = {max(window)}")
    
    print()

# ============================================================
# BONUS CHALLENGE: LRU Cache
# ============================================================

class LRUCache:
    """
    Least Recently Used (LRU) cache using deque.
    
    TODO: Implement LRU cache with maxsize
    """
    
    def __init__(self, maxsize: int):
        self.cache = {}
        self.order = deque()
        self.maxsize = maxsize
    
    def get(self, key: Any) -> Any:
        """Get value and mark as recently used"""
        if key not in self.cache:
            return None
        
        # Move to end (most recent)
        self.order.remove(key)
        self.order.append(key)
        
        return self.cache[key]
    
    def put(self, key: Any, value: Any):
        """Put value in cache"""
        if key in self.cache:
            # Update existing
            self.order.remove(key)
        elif len(self.cache) >= self.maxsize:
            # Evict least recently used
            lru_key = self.order.popleft()
            del self.cache[lru_key]
        
        self.cache[key] = value
        self.order.append(key)
    
    def __repr__(self):
        return f"LRUCache({dict(zip(self.order, [self.cache[k] for k in self.order]))})"

def test_lru_cache():
    """Test LRU cache"""
    print("--- Bonus Challenge: LRU Cache ---")
    
    cache = LRUCache(maxsize=3)
    
    print("Adding items:")
    cache.put('a', 1)
    print(f"  Put a=1: {cache}")
    cache.put('b', 2)
    print(f"  Put b=2: {cache}")
    cache.put('c', 3)
    print(f"  Put c=3: {cache}")
    
    print("\nAccessing 'a' (marks as recent):")
    val = cache.get('a')
    print(f"  Got a={val}: {cache}")
    
    print("\nAdding 'd' (evicts 'b'):")
    cache.put('d', 4)
    print(f"  Put d=4: {cache}")
    
    print("\nTrying to get 'b' (evicted):")
    val = cache.get('b')
    print(f"  Got b={val}")
    
    print()

# ============================================================
# COMPLEXITY ANALYSIS
# ============================================================

def complexity_notes():
    """
    Time & Space Complexity:
    
    deque Operations:
    - append/appendleft: O(1)
    - pop/popleft: O(1)
    - Access by index: O(n) - not efficient!
    - rotate: O(k) where k is rotation amount
    - extend/extendleft: O(k) where k is items added
    
    vs List:
    - list.append: O(1) amortized
    - list.insert(0, x): O(n) - slow!
    - list.pop(): O(1)
    - list.pop(0): O(n) - slow!
    
    Space Complexity:
    - O(n) for n elements
    - Bounded deque: O(maxlen)
    
    Benefits:
    - Fast operations at both ends
    - Thread-safe append/pop
    - Memory efficient
    - Great for queues, stacks, sliding windows
    
    Use Cases:
    - Queue implementation (FIFO)
    - Stack implementation (LIFO)
    - Sliding window problems
    - Recent history tracking
    - Round-robin scheduling
    - Undo/redo functionality
    
    When NOT to Use:
    - Need random access by index
    - Need to search/sort frequently
    - Small datasets where list is fine
    
    Security Considerations:
    - Bounded deque prevents memory exhaustion
    - Use maxlen for user-facing queues
    - Be careful with rotation on large deques
    """
    pass

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Week 3, Day 2: deque")
    print("=" * 60)
    print()
    
    deque_basics()
    performance_comparison()
    rotation_operations()
    bounded_deque()
    test_queue()
    test_stack()
    test_browser_history()
    test_sliding_window()
    test_lru_cache()
    
    print("=" * 60)
    print("✅ Day 2 Complete!")
    print("=" * 60)
    print("\n💡 Key Takeaways:")
    print("1. deque provides O(1) append/pop from both ends")
    print("2. Much faster than list for operations at beginning")
    print("3. rotate() is perfect for round-robin scheduling")
    print("4. maxlen creates bounded deque (auto-evicts old items)")

